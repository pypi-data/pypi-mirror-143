"""
    DigiCloud Edge SND and CDN services.
"""
import json
import os

from marshmallow.exceptions import ValidationError
from rich.prompt import Confirm

from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError
from .. import schemas
from ..utils import is_tty


class ListDomain(Lister):
    """List edge domains"""
    schema = schemas.EdgeDomainList(many=True)

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/domains')
        return domains


class CreateDomain(ShowOne):
    """Create Domain"""
    schema = schemas.EdgeDomainDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Domain name'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
        }
        domain = self.app.session.post('/edge/domains', payload)
        nslookup_urls = (
            "ns1.digikalacloud.com",
            "ns2.digikalacloud.com",
        )
        self.app.console.print(
            "[green bold] Attention: \n Please change your domain NS records to"
            " {} .[green bold]".format(" and ".join(nslookup_urls))
        )
        return domain


class DeleteDomain(Command):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id'
        )

        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        if not self.confirm_domain_deletion(parsed_args):
            return
        self.app.session.delete('/edge/domains/%s' % parsed_args.domain)

    def confirm_domain_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
            user_response = Confirm.ask(
                "You're about to delete domain named [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    domain['name']
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'domain delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False


class ShowDomain(ShowOne):
    schema = schemas.EdgeDomainDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id'
        )
        return parser

    def get_data(self, parsed_args):
        domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
        return domain


def t_or_f_or_n(arg):
    upper_arg = str(arg).upper()
    if 'TRUE'.startswith(upper_arg):
        return True
    elif 'FALSE'.startswith(upper_arg):
        return False
    else:
        return None


def get_record_schema(data):
    schema_map = {
        "A": schemas.ARecordDetailsSchema(),
        "TXT": schemas.TXTRecordDetailsSchema(),
        "CNAME": schemas.CNAMERecordDetailsSchema(),
        "MX": schemas.MXRecordDetailsSchema(),
        "SRV": schemas.SRVRecordDetailsSchema(),
    }
    return schema_map.get(data["type"], None)


class ListRecord(Lister):
    """List edge records"""
    schema = schemas.RecordListSchema(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/domains/{}/records'.format(parsed_args.domain))
        return domains


class ShowRecord(ShowOne):
    """Show domain details."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        record = self.app.session.get(uri)
        self.schema = get_record_schema(record)
        return record


class DeleteRecord(Command):
    """Delete record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        self.app.session.delete(uri)


class UpdateRecord(ShowOne):
    """Update record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required=False,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=False,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        record = self.app.session.patch(uri, payload)
        self.schema = get_record_schema(record)
        return record


class CreateRecord(ShowOne):
    """Create Record"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required = True,
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help='Record type.',
            choices=("A", "TXT", "CNAME", "MX", "SRV",),
            required=True,
            type=str.upper,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=True,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        try:
            payload = self._get_record_type_schema(payload["type"])().load(payload)
        except ValidationError as e:
            raise CLIError(self._handle_validation_error(payload["type"], e))
        record = self.app.session.post('/edge/domains/{}/records'.format(parsed_args.domain), payload)
        self.schema = get_record_schema(record)
        return record

    @staticmethod
    def _handle_validation_error(record_type: str, e: ValidationError):
        errors = []
        for key, value in e.messages.items():
            error = "".join(value)
            if error == "Unknown field.":
                msg = "can not use --{} with {} record type.".format(key, record_type)
            elif error == "Missing data for required field.":
                msg = "--{} is required by {} record type.".format(
                    key.replace("_", "-"),
                    record_type
                )
            else:
                raise NotImplementedError
            errors.append(dict(
                msg=msg
            ))
        return errors

    @staticmethod
    def _get_record_type_schema(record_type: str):
        record_schema_map = {
            "A": schemas.ARecordDetailsSchema,
            "TXT": schemas.TXTRecordDetailsSchema,
            "MX": schemas.MXRecordDetailsSchema,
            "CNAME": schemas.CNAMERecordDetailsSchema,
            "SRV": schemas.SRVRecordDetailsSchema,
        }
        return record_schema_map[record_type]


class ListUpstream(Lister):
    """List edge upstreams"""
    schema = schemas.UpstreamDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        upstreams = self.app.session.get('/edge/domains/{}/upstreams'.format(parsed_args.domain))
        return upstreams


class ShowUpstream(ShowOne):
    """Show upstream details."""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        upstream = self.app.session.get(uri)
        return upstream


class DeleteUpstream(Command):
    """Delete upstream."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        self.app.session.delete(uri)


class UpdateUpstream(ShowOne):
    """Update upstream."""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
        )
        parser.add_argument(
            '--lb-method',
            metavar='<lb-method>',
            help='Load balancing method.',
            choices=("consistent_ip_hash", "round_robin",),
            type=str.lower,
        )
        parser.add_argument(
            '--keep-alive',
            metavar='<keep-alive>',
            help='keep alive time.',
        )
        parser.add_argument(
            '--ssl-policy',
            metavar='<ssl-policy>',
            help='SSL policy.',
            choices=("http", "https",),
            type=str.lower,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.lb_method:
            payload["lb_method"] = parsed_args.lb_method
        if parsed_args.keep_alive:
            payload["keep_alive"] = parsed_args.keep_alive
        if parsed_args.ssl_policy:
            payload["ssl_policy"] = parsed_args.ssl_policy
        upstream = self.app.session.patch(uri, payload)
        return upstream


class CreateUpstream(ShowOne):
    """Create upstream"""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
            required=True,
        )
        parser.add_argument(
            '--lb-method',
            metavar='<lb-method>',
            help='Load balancing method.',
            choices=("consistent_ip_hash", "round_robin",),
            required=True,
            type=str.lower,
        )
        parser.add_argument(
            '--keep-alive',
            metavar='<keep-alive>',
            help='keep alive time.',
            required=True,
        )
        parser.add_argument(
            '--ssl-policy',
            metavar='<ssl-policy>',
            help='SSL policy.',
            choices=("http", "https",),
            required=True,
            type=str.lower,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/upstreams'.format(parsed_args.domain)
        payload = {
            "name": parsed_args.name,
            "lb_method": parsed_args.lb_method,
            "keep_alive": parsed_args.keep_alive,
            "ssl_policy": parsed_args.ssl_policy,
        }
        upstream = self.app.session.post(url, payload)
        return upstream


class ListUpstreamServer(Lister):
    """List edge upstream servers"""
    schema = schemas.UpstreamServerDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        servers = self.app.session.get(
            '/edge/domains/{}/upstreams/{}/servers'.format(
                parsed_args.domain,
                parsed_args.upstream,
            ))
        return servers


class ShowUpstreamServer(ShowOne):
    """Show upstream server details."""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        server = self.app.session.get(uri)
        return server


class DeleteUpstreamServer(Command):
    """Delete upstream server."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        self.app.session.delete(uri)


class UpdateUpstreamServer(ShowOne):
    """Update upstream server."""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        parser.add_argument(
            '--ip-domain',
            metavar='<ip-domain>',
            help='Server ip domain.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Server port.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='server weight.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--fail-timeout',
            metavar='<fail-timeout>',
            help='Server fail timeout.',
            required=True,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        payload = {}
        if parsed_args.ip_domain:
            payload["ip_domain"] = parsed_args.ip_domain
        if parsed_args.port:
            payload["port"] = parsed_args.port
        if parsed_args.weight:
            payload["weight"] = parsed_args.weight
        if parsed_args.fail_timeout:
            payload["fail_timeout"] = parsed_args.fail_timeout
        server = self.app.session.patch(uri, payload)
        return server


class CreateUpstreamServer(ShowOne):
    """Create upstream server"""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        parser.add_argument(
            '--ip-domain',
            metavar='<ip-domain>',
            help='Server ip domain.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Server port.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='server weight.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--fail-timeout',
            metavar='<fail-timeout>',
            help='Server fail timeout.',
            required=True,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/upstreams/{}/servers'.format(parsed_args.domain, parsed_args.upstream)
        payload = {
            "ip_domain": parsed_args.ip_domain,
            "port": parsed_args.port,
            "weight": parsed_args.weight,
            "fail_timeout": parsed_args.fail_timeout,
        }
        server = self.app.session.post(url, payload)
        return server


class ShowSSL(ShowOne):
    """Show ssl details."""
    schema = schemas.SSLDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain name ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/ssl'.format(parsed_args.domain)
        ssl = self.app.session.get(uri)
        return ssl


class UpdateSSL(ShowOne):
    """Update ssl."""
    schema = schemas.SSLDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain ID or name',
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help='SSL type.',
            choices=("custom",),
        )
        parser.add_argument(
            '--policy',
            metavar='<policy>',
            help='SSL policy.',
            choices=("normal", "strict",),
        )
        parser.add_argument(
            '--enable',
            metavar='<enable>',
            help='SSL enable.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--hsts',
            metavar='<hsts>',
            help='SSL hsts.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--https-redirect',
            metavar='<https-redirect>',
            help='SSL https redirect.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--private-key',
            metavar='<private-key>',
            help='SSL private-key filename.',
        )
        parser.add_argument(
            '--public-key',
            metavar='<public-key>',
            help='SSL public-key filename.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/ssl'.format(
            parsed_args.domain,
        )
        payload = {}
        if parsed_args.type:
            payload["type"] = parsed_args.type
        if parsed_args.policy:
            payload["policy"] = parsed_args.policy
        if parsed_args.enable is not None:
            payload["enable"] = parsed_args.enable
        if parsed_args.hsts is not None:
            payload["hsts"] = parsed_args.hsts
        if parsed_args.https_redirect is not None:
            payload["https_redirect"] = parsed_args.https_redirect
        if parsed_args.public_key:
            with open(os.path.expanduser(parsed_args.public_key)) as file_:
                payload["public_key"] = file_.read()
        if parsed_args.private_key:
            with open(os.path.expanduser(parsed_args.private_key)) as file_:
                payload["private_key"] = file_.read()
        server = self.app.session.patch(uri, payload)
        return server


def t_or_f_or_n(arg):
    upper_arg = str(arg).upper()
    if 'TRUE'.startswith(upper_arg):
        return True
    elif 'FALSE'.startswith(upper_arg):
        return False
    else:
        return None


class ListLocation(Lister):
    """List edge locations"""
    schema = schemas.LocationDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        locations = self.app.session.get('/edge/domains/{}/locations'.format(parsed_args.domain))
        return locations


class ShowLocation(ShowOne):
    """Show location details."""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        location = self.app.session.get(uri)
        return location


class DeleteLocation(Command):
    """Delete location."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        self.app.session.delete(uri)


class UpdateLocation(ShowOne):
    """Update location."""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='edge location path.',
        )
        parser.add_argument(
            '--path-type',
            metavar='<path-type>',
            help='location path type.',
            choices=("explicit", "prefix", "extension",),
            type=str.lower,
        )
        parser.add_argument(
            '--path-extensions',
            metavar='<path-extensions>',
            help='List location path extensions.',
            nargs='+',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='location upstream.',
        )
        parser.add_argument(
            '--origin-headers',
            metavar='<origin-headers>',
            help='location origin headers.',
        )
        parser.add_argument(
            '--response-headers',
            metavar='<response-headers>',
            help='location response headers.',
        )
        parser.add_argument(
            '--cache-enabled',
            metavar='<cache-enabled>',
            help='location cache enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--cache-ttl',
            metavar='<cache-ttl>',
            help='location cache time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h", "1d", "2d", "1w", "1M",),
        )
        parser.add_argument(
            '--cache-key',
            metavar='<cache-key>',
            help='location cache key.',
            choices=("u", "uq", "uqc",),
            type=str.lower,
        )
        parser.add_argument(
            '--cache-cookie-name',
            metavar='<cache-cookie-name>',
            help='location cache cookie name.',
        )
        parser.add_argument(
            '--cache-zone',
            metavar='<cache-zone>',
            help='location cache zone id.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.path:
            payload["path"] = parsed_args.path
        if parsed_args.path_type:
            payload["path_type"] = parsed_args.path_type
        if parsed_args.path_extensions:
            payload["path_extensions"] = parsed_args.path_extensions
        if parsed_args.upstream:
            payload["upstream"] = parsed_args.upstream
        if parsed_args.origin_headers:
            with open(os.path.expanduser(parsed_args.origin_headers)) as file_:
                origin_headers_content = file_.read()
                try:
                    payload["origin_headers"] = json.loads(origin_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="origin-headers is not a valid json")])
        if parsed_args.response_headers:
            with open(os.path.expanduser(parsed_args.response_headers)) as file_:
                response_headers_content = file_.read()
                try:
                    payload["response_headers"] = json.loads(response_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="response-headers is not a valid json")])
        if parsed_args.cache_enabled is not None:
            payload["cache_enabled"] = parsed_args.cache_enabled
        if parsed_args.cache_ttl:
            payload["cache_ttl"] = parsed_args.cache_ttl
        if parsed_args.cache_key:
            payload["cache_key"] = parsed_args.cache_key
        if parsed_args.cache_cookie_name:
            payload["cache_cookie_name"] = parsed_args.cache_cookie_name
        if parsed_args.cache_zone:
            payload["cache_zone"] = parsed_args.cache_zone
        location = self.app.session.patch(uri, payload)
        return location


class CreateLocation(ShowOne):
    """Create location"""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
            required=True,
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='edge location path.',
            required=True,
        )
        parser.add_argument(
            '--path-type',
            metavar='<path-type>',
            help='location path type.',
            choices=("explicit", "prefix", "extension",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--path-extensions',
            metavar='<path-extensions>',
            help='List of location path extensions.',
            nargs='+',
            required=False,
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='location upstream id.',
            required=True,
        )
        parser.add_argument(
            '--origin-headers',
            metavar='<origin-headers>',
            help='location origin headers.',
        )
        parser.add_argument(
            '--response-headers',
            metavar='<response-headers>',
            help='location response headers.',
        )
        parser.add_argument(
            '--cache-enabled',
            metavar='<cache-enabled>',
            help='location cache enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--cache-ttl',
            metavar='<cache-ttl>',
            help='location cache time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h", "1d", "2d", "1w", "1M",),
        )
        parser.add_argument(
            '--cache-key',
            metavar='<cache-key>',
            help='location cache key.',
            choices=("u", "uq", "uqc",),
            type=str.lower,
        )
        parser.add_argument(
            '--cache-cookie-name',
            metavar='<cache-cookie-name>',
            help='location cache cookie name.',
        )
        parser.add_argument(
            '--cache-zone',
            metavar='<cache-zone>',
            help='location cache zone id.',
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/locations'.format(parsed_args.domain)
        payload = {
            "name": parsed_args.name,
            "path": parsed_args.path,
            "path_type": parsed_args.path_type,
            "upstream_id": parsed_args.upstream,
        }
        if parsed_args.path_extensions:
            payload["path_extensions"] = parsed_args.path_extensions
        if parsed_args.origin_headers:
            with open(os.path.expanduser(parsed_args.origin_headers)) as file_:
                origin_headers_content = file_.read()
                try:
                    payload["origin_headers"] = json.loads(origin_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="origin-headers is not a valid json")])
        if parsed_args.response_headers:
            with open(os.path.expanduser(parsed_args.response_headers)) as file_:
                response_headers_content = file_.read()
                try:
                    payload["response_headers"] = json.loads(response_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="response-headers is not a valid json")])
        if parsed_args.cache_enabled is not None:
            payload["cache_enabled"] = parsed_args.cache_enabled
        if parsed_args.cache_ttl:
            payload["cache_ttl"] = parsed_args.cache_ttl
        if parsed_args.cache_key:
            payload["cache_key"] = parsed_args.cache_key
        if parsed_args.cache_cookie_name:
            payload["cache_cookie_name"] = parsed_args.cache_cookie_name
        if parsed_args.cache_zone:
            payload["cache_zone"] = parsed_args.cache_zone
        location = self.app.session.post(url, payload)
        return location


class ListFirewall(Lister):
    """List edge firewalls"""
    schema = schemas.EdgeFirewallDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        firewalls = self.app.session.get('/edge/domains/{}/firewalls'.format(parsed_args.domain))
        return firewalls


class ShowFirewall(ShowOne):
    """Show firewall details."""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        firewall = self.app.session.get(uri)
        return firewall


class DeleteFirewall(Command):
    """Delete firewall."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        self.app.session.delete(uri)


class UpdateFirewall(ShowOne):
    """Update firewall."""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help='firewall rule input type.',
            choices=("ip", "asn", "country", "continent",),
            type=str.lower,
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            help='firewall rule value path.',
        )
        parser.add_argument(
            '--action',
            metavar='<action>',
            help='firewall rule action.',
            choices=("allow", "block", "javascript_challenge", "captcha_challenge",),
            type=str.lower,
        )
        parser.add_argument(
            '--operator',
            metavar='<operator>',
            help='firewall rule operator',
            choices=("eq", "neq",),
            type=str.lower,
        )
        parser.add_argument(
            '--location',
            metavar='<location>',
            help='firewall location id.',
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='firewall rule priority.',
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        payload = {}
        if parsed_args.input:
            payload["input"] = parsed_args.input
        if parsed_args.value:
            payload["value"] = parsed_args.value
        if parsed_args.action:
            payload["action"] = parsed_args.action
        if parsed_args.operator:
            payload["operator"] = parsed_args.operator
        if parsed_args.location:
            payload["location"] = parsed_args.location
        if parsed_args.priority:
            payload["priority"] = parsed_args.priority
        location = self.app.session.patch(uri, payload)
        return location


class CreateFirewall(ShowOne):
    """Create firewall"""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help='firewall rule input type.',
            choices=("ip", "asn", "country", "continent",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            help='firewall rule value path.',
            required=True,
        )
        parser.add_argument(
            '--action',
            metavar='<action>',
            help='firewall rule action.',
            choices=("allow", "block", "javascript_challenge", "captcha_challenge",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--operator',
            metavar='<operator>',
            help='firewall rule operator',
            choices=("eq", "neq",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--location',
            metavar='<location>',
            help='firewall location id.',
            required=True,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='firewall rule priority.',
            type=int,
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/firewalls'.format(parsed_args.domain)
        payload = {
            "input": parsed_args.input,
            "value": parsed_args.value,
            "action": parsed_args.action,
            "operator": parsed_args.operator,
            "location_id": parsed_args.location,
            "priority": parsed_args.priority,
        }
        location = self.app.session.post(url, payload)
        return location


class ListCacheZone(Lister):
    """List edge cache zones"""
    schema = schemas.CacheZoneList(many=True)

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/cache-zones')
        return domains
