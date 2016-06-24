# -*- coding: utf-8 -*-

from decouple import config
from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    """
    python manage.py oauth
    """

    help = 'Setup GitHub OAuth.'

    def handle(self, *args, **options):
        social_app = SocialApp.objects.get_or_create(
            client_id=config('GITHUB_CLIENT_ID'),
            secret=config('GITHUB_CLIENT_SECRET'),
            name=config('PROJECT_NAME', default='lend').title(),
            provider='github',
        )[0]
        social_app.sites.add(
            Site.objects.get_or_create(
                domain=config('SITE_URL', default='example.com'),
                name=config('SITE_NAME', default='example.com')
            )[0]
        )
        print('GitHub OAuth Successfully configurated.')
