# Only run this script in development

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User
from auction.models import Auction, Bid, Like, Comment
from django.utils import timezone


class Command(BaseCommand):
    help = "Resets the database, runs migrations, and seeds initial data (5 users, 3 auctions)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "This command will DROP ALL DATA in your database."))
        confirm = input("Are you sure you want to proceed? (y/[n]): ").lower()

        if confirm != 'y' and confirm != 'yes':
            self.stdout.write(self.style.ERROR("Operation cancelled."))
            return

        # Determine the database type and delete the database file if it's SQLite
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            db_path = settings.DATABASES['default']['NAME']
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS(
                    f"Deleted SQLite database file: {db_path}"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"SQLite database file not found: {db_path}"))
        elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            # For postgres, we just migrate.  The database should have been created already.
            self.stdout.write(self.style.SUCCESS(
                "Postgres database will be cleared by migrations."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Database type not recognized.  Ensure it is manually cleared if needed."))

        self.stdout.write("Running makemigrations for auction and user...")
        call_command('makemigrations', 'auction')
        call_command('makemigrations', 'user')

        self.stdout.write("Running migrations...")
        call_command('migrate')  # Run migrate without --fake

        self.stdout.write("Seeding database...")
        self.seed_database()
        self.stdout.write(self.style.SUCCESS(
            "Database reset and seeded successfully."))

    def seed_database(self):
        """
        Seeds the database with 5 users and 3 auctions, all owned by the first user.
        """
        # Create 5 users
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password=f'password{i}',
                first_name='user',
                last_name=f'{i}'
            )
            users.append(user)

        # Create 3 auctions, all owned by user1
        auctions = []
        for i in range(1, 4):
            auction = Auction.objects.create(
                seller=users[0],  # User1 owns all auctions
                title=f'Auction {i}',
                description=f'Description for Auction {i}',
                image_url='https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg',
                starting_price=10.00 * i,
                end_time=timezone.now() + timezone.timedelta(days=10 - i)
            )
            auctions.append(auction)

        # Seed bids
        for i, user in enumerate(users[1:]):
            Bid.objects.create(
                bidder=user,
                auction=auctions[1],
                amount=auctions[1].starting_price + 10.00 * (i + 1)
            )

        # Seed likes (users 2-5 like the first auction)
        for user in users[1:]:  # Users 2, 3, 4, 5
            Like.objects.create(
                user=user,
                auction=auctions[0],  # First auction
            )

        # Seed comments (users 3-5 comment on the second auction)
        for user in users[2:]:  # Users 3, 4, 5
            Comment.objects.create(
                user=user,
                auction=auctions[1],  # Second auction
                comment_text=f'Nice pic!! by {user.username}',
            )
