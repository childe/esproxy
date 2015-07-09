""" Django CAS 2.0 authentication backend """

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User,Group
from django_cas.exceptions import CasTicketException
from django_cas.models import Tgt, PgtIOU
from urllib import urlencode, urlopen
from urlparse import urljoin
from xml.dom import minidom
import logging
import time

__all__ = ['CASBackend']

logger = logging.getLogger(__name__)

class CASBackend(ModelBackend):
    """ CAS authentication backend """

    def authenticate(self, ticket, service):
        """ Verifies CAS ticket and gets or creates User object """

        (username, proxies,mail,department,company,employee,sn) = self._verify(ticket, service)
        if not username:
            return None

        if settings.CAS_ALLOWED_PROXIES:
            for proxy in proxies:
                if not proxy in settings.CAS_ALLOWED_PROXIES:
                    return None

        logger.debug("User '%s' passed authentication by CAS backend", username)

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            if settings.CAS_AUTO_CREATE_USERS:
                logger.debug("User '%s' auto created by CAS backend", username)
                try:
                    user=User.objects.create_user(username=username,email=mail,first_name=employee,last_name=sn)
                except:
                    user=User.objects.create(username=username,email=mail,first_name=employee,last_name=sn)
                group,created=Group.objects.get_or_create(name=department)
                user.groups=[group]
                user.save()
                return user
            else:
                logger.error("Failed authentication, user '%s' does not exist", username)
        return None

    def _verify(self, ticket, service):
        """ Verifies CAS 2.0+ XML-based authentication ticket.

            Returns tuple (username, [proxy URLs]) on success or None on failure.
        """
        params = {'ticket': ticket, 'service': service}
        if settings.CAS_PROXY_CALLBACK:
            params.update({'pgtUrl': settings.CAS_PROXY_CALLBACK})
        if settings.CAS_RENEW:
            params.update({'renew': 'true'})

        page = urlopen(urljoin(settings.CAS_SERVER_URL, 'proxyValidate') + '?' + urlencode(params))

        try:
            readc=page.read()
            response = minidom.parseString(readc)
            if response.getElementsByTagName('cas:authenticationFailure'):
                logger.warn("Authentication failed from CAS server: %s",
                            response.getElementsByTagName('cas:authenticationFailure')[0].firstChild.nodeValue)
                return (None, None, None, None, None, None,None)

            username = response.getElementsByTagName('cas:user')[0].firstChild.nodeValue
            proxies = []
            if response.getElementsByTagName('cas:proxyGrantingTicket'):
                proxies = [p.firstChild.nodeValue for p in response.getElementsByTagName('cas:proxies')]
                pgt = response.getElementsByTagName('cas:proxyGrantingTicket')[0].firstChild.nodeValue
                try:
                    pgtIou = self._get_pgtiou(pgt)
                    tgt = Tgt.objects.get(username = username)
                    tgt.tgt = pgtIou.tgt
                    tgt.save()
                    pgtIou.delete()
                except Tgt.DoesNotExist:
                    Tgt.objects.create(username = username, tgt = pgtIou.tgt)
                    pgtIou.delete()
                except:
                    logger.error("Failed to do proxy authentication.", exc_info=True)

            logger.debug("Cas proxy authentication succeeded for %s with proxies %s", username, proxies)
            mail = response.getElementsByTagName('cas:mail')
            if mail:
                mail = mail[0].firstChild.nodeValue
            else:
                mail = None
            department = response.getElementsByTagName('cas:department')
            if department:
                department=department[0].firstChild.nodeValue
            company = response.getElementsByTagName('cas:company')
            if company:
                company=company[0].firstChild.nodeValue
            employee = response.getElementsByTagName('cas:employee')
            if employee:
                employee=employee[0].firstChild.nodeValue
            sn = response.getElementsByTagName('cas:sn')[0].firstChild.nodeValue
            return (username, proxies,mail,department,company,employee,sn)
        except Exception as e:
            logger.error("Failed to verify CAS authentication", e)
            return (None, None, None, None, None, None, None)
        finally:
            page.close()


    def _get_pgtiou(self, pgt):
        """ Returns a PgtIOU object given a pgt.

            The PgtIOU (tgt) is set by the CAS server in a different request that has
            completed before this call, however, it may not be found in the database
            by this calling thread, hence the attempt to get the ticket is retried
            for up to 5 seconds. This should be handled some better way.
        """
        pgtIou = None
        retries_left = 5
        while not pgtIou and retries_left:
            try:
                return PgtIOU.objects.get(pgtIou=pgt)
            except PgtIOU.DoesNotExist:
                time.sleep(1)
                retries_left -= 1
        raise CasTicketException("Could not find pgtIou for pgt %s" % pgt)
