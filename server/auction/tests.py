from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, force_authenticate
from .models import Auction, Bid, Like, Comment
from .serializers import AuctionDetailSerializer


class AuctionListViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
                   Status  | Start Price | Highest Bid | Bid | Like | Comment
        auction1:  Active  |    10.00    |    15.00    |  1  |  2   |    0
        auction2: Inactive |    20.00    |    None     |  0  |  0   |    1
        auction3:  Active  |    15.00    |    None     |  0  |  1   |    0
        """

        cls.user1 = User.objects.create_user(
            username='user1', password='password1')
        cls.user2 = User.objects.create_user(
            username='user2', password='password2')
        cls.user3 = User.objects.create_user(
            username='user3', password='password3')

        cls.auction1 = Auction.objects.create(
            seller=cls.user1,
            title='Active Auction 1',
            description='Description for Active Auction 1',
            starting_price=10.00,
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )
        cls.auction2 = Auction.objects.create(
            seller=cls.user1,
            title='Inactive Auction 2',
            description='Description for Inactive Auction 2',
            starting_price=20.00,
            end_time=timezone.now() - timezone.timedelta(days=1),
            is_active=False,
        )
        cls.auction3 = Auction.objects.create(
            seller=cls.user2,
            title='Active Auction 3',
            description='Description for Active Auction 3',
            starting_price=15.00,
            end_time=timezone.now() + timezone.timedelta(days=2),
            is_active=True
        )

        cls.bid1 = Bid.objects.create(
            bidder=cls.user2, auction=cls.auction1, amount=15.00)

        cls.like1 = Like.objects.create(
            user=cls.user2, auction=cls.auction1)
        cls.like2 = Like.objects.create(
            user=cls.user3, auction=cls.auction1)
        cls.like3 = Like.objects.create(
            user=cls.user1, auction=cls.auction3)

        cls.comment1 = Comment.objects.create(
            user=cls.user1, auction=cls.auction2, comment_text="Comment 1")

    def test_auction_list_all(self):
        """
        Test that the auction list endpoint returns all auctions when no filter is provided.
        """
        url = reverse('auction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that all 3 auctions are returned
        self.assertEqual(len(response.data), 3)

        auction_data = response.data[0]
        self.assertIn('highest_bid', auction_data)
        self.assertIn('bid_count', auction_data)
        self.assertIn('like_count', auction_data)
        self.assertIn('comment_count', auction_data)
        self.assertEqual(auction_data['highest_bid'], 15.00)
        self.assertEqual(auction_data['bid_count'], 1)
        self.assertEqual(auction_data['like_count'], 2)
        self.assertEqual(auction_data['comment_count'], 0)

        auction_data_no_bid = response.data[1]
        self.assertEqual(auction_data_no_bid['highest_bid'], None)

    def test_auction_list_active(self):
        """
        Test that the auction list endpoint returns only active auctions when is_active=true.
        """
        url = reverse('auction_list') + '?is_active=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that only 2 active auctions are returned
        self.assertEqual(len(response.data), 2)
        auction_titles = [auction['title'] for auction in response.data]
        self.assertIn('Active Auction 1', auction_titles)
        self.assertIn('Active Auction 3', auction_titles)
        self.assertNotIn('Inactive Auction 2', auction_titles)

        auction_data = response.data[0]
        self.assertIn('highest_bid', auction_data)
        self.assertIn('bid_count', auction_data)
        self.assertIn('like_count', auction_data)
        self.assertIn('comment_count', auction_data)
        self.assertEqual(auction_data['highest_bid'], 15.00)
        self.assertEqual(auction_data['bid_count'], 1)
        self.assertEqual(auction_data['like_count'], 2)
        self.assertEqual(auction_data['comment_count'], 0)

    def test_auction_list_inactive(self):
        """
        Test that the auction list endpoint returns only inactive auctions when is_active=false.
        """
        url = reverse('auction_list') + '?is_active=false'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that only 1 inactive auction is returned
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Inactive Auction 2')

        auction_data = response.data[0]
        self.assertIn('highest_bid', auction_data)
        self.assertIn('bid_count', auction_data)
        self.assertIn('like_count', auction_data)
        self.assertIn('comment_count', auction_data)
        self.assertIsNone(auction_data['highest_bid'])
        self.assertEqual(auction_data['bid_count'], 0)
        self.assertEqual(auction_data['like_count'], 0)
        self.assertEqual(auction_data['comment_count'], 1)

    def test_auction_list_invalid_filter(self):
        """
        Test that the auction list endpoint returns a 400 error for an invalid is_active value.
        """
        url = reverse('auction_list') + '?is_active=invalid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            "Invalid query parameter for is_active."
        )

    def test_auction_list_default(self):
        """
        Test that the auction list endpoint returns all auctions when no filter is provided
        """
        url = reverse('auction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        auction_data = response.data[0]
        self.assertIn('highest_bid', auction_data)
        self.assertIn('bid_count', auction_data)
        self.assertIn('like_count', auction_data)
        self.assertIn('comment_count', auction_data)
        self.assertEqual(auction_data['highest_bid'], 15.00)
        self.assertEqual(auction_data['bid_count'], 1)
        self.assertEqual(auction_data['like_count'], 2)
        self.assertEqual(auction_data['comment_count'], 0)


class AuctionDetailViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
                   Status  | Start Price | Highest Bid | Bid | Like | Comment
        auction1:  Active  |    10.00    |    25.00    |  2  |  1   |    2
        auction2: Inactive |    20.00    |    None     |  0  |  0   |    0
        """

        cls.user1 = User.objects.create_user(
            username='user1', password='password1')
        cls.user2 = User.objects.create_user(
            username='user2', password='password2')
        cls.user3 = User.objects.create_user(
            username='user3', password='password3')

        cls.auction1 = Auction.objects.create(
            seller=cls.user1,
            title='Active Auction 1',
            description='Description for Active Auction 1',
            starting_price=10.00,
            end_time=timezone.now() + timezone.timedelta(days=1),  # Active auction
            is_active=True,
        )
        cls.auction2 = Auction.objects.create(
            seller=cls.user1,
            title='Inactive Auction 2',
            description='Description for Inactive Auction 2',
            starting_price=20.00,
            end_time=timezone.now() - timezone.timedelta(days=1),
            is_active=False,
        )

        cls.bid1 = Bid.objects.create(
            bidder=cls.user2, auction=cls.auction1, amount=15.00)
        cls.bid2 = Bid.objects.create(
            bidder=cls.user3, auction=cls.auction1, amount=25.00)

        cls.like1 = Like.objects.create(user=cls.user2, auction=cls.auction1)

        cls.comment1 = Comment.objects.create(
            user=cls.user2, auction=cls.auction1, comment_text="Comment 1")
        cls.comment2 = Comment.objects.create(
            user=cls.user3, auction=cls.auction1, comment_text="Comment 2")

    def test_auction_detail_view(self):
        """
        Test that the auction detail endpoint returns the correct data.
        """
        url = reverse('auction_detail', kwargs={'pk': self.auction1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.auction1.pk)
        self.assertEqual(response.data['title'], self.auction1.title)

    def test_auction_detail_serializer_methods(self):
        """
        Test the methods of the AuctionDetailSerializer.
        """
        # Create a mock request
        mock_request = self.client.request()
        # Set the user on the mock request
        setattr(mock_request, 'user', self.user1)

        # Initialize the serializer with the auction instance and context
        serializer = AuctionDetailSerializer(
            instance=self.auction1, context={'request': mock_request})

        # Test get_bids
        bids_data = serializer.get_bids(self.auction1)
        self.assertEqual(len(bids_data), 2)
        self.assertEqual(bids_data[0], 25.00)
        self.assertEqual(bids_data[1], 15.00)

        # Test get_bid_count
        bid_count = serializer.get_bid_count(self.auction1)
        self.assertEqual(bid_count, 2)

        # Test get_like_count
        like_count = serializer.get_like_count(self.auction1)
        self.assertEqual(like_count, 1)

        # Test get_comment_count
        comment_count = serializer.get_comment_count(self.auction1)
        self.assertEqual(comment_count, 2)

        # Test get_highest_bid
        highest_bid = serializer.get_highest_bid(self.auction1)
        self.assertEqual(highest_bid, 25.00)

        # Test get_user_has_liked (user has not liked)
        user_has_liked = serializer.get_user_has_liked(self.auction1)
        self.assertFalse(user_has_liked)

        # Test get_user_has_liked (user has liked)
        # User 1 likes auction 1
        Like.objects.create(user=self.user1, auction=self.auction1)
        user_has_liked = serializer.get_user_has_liked(self.auction1)
        self.assertTrue(user_has_liked)


class AuctionCreateViewTests(APITestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('auction_create')

    def test_create_auction_success(self):
        """
        Test successful auction creation with valid data.
        """
        force_authenticate(self.client, user=self.user)
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': 100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Auction.objects.count(), 1)
        auction = Auction.objects.get(title='Test Auction')
        self.assertEqual(auction.seller, self.user)
        self.assertEqual(auction.description, 'This is a test auction.')
        self.assertEqual(auction.starting_price, 100.00)
        self.assertEqual(auction.end_time, end_time)
        self.assertTrue(auction.is_active)

    def test_create_auction_missing_title(self):
        """
        Test auction creation with missing title.
        """
        force_authenticate(self.client, user=self.user)
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'description': 'This is a test auction.',
            'starting_price': 100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_auction_missing_description(self):
        """
        Test auction creation with missing description.
        """
        force_authenticate(self.client, user=self.user)  # Authenticate
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'starting_price': 100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('description', response.data)

    def test_create_auction_missing_starting_price(self):
        """
        Test auction creation with missing starting price.
        """
        force_authenticate(self.client, user=self.user)  # Authenticate
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('starting_price', response.data)

    def test_create_auction_missing_end_time(self):
        """
        Test auction creation with missing end time.
        """
        force_authenticate(self.client, user=self.user)  # Authenticate
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': 100.00,
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_time', response.data)

    def test_create_auction_invalid_starting_price(self):
        """
        Test auction creation with an invalid starting price (e.g., negative value).
        """
        force_authenticate(self.client, user=self.user)
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': -100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('starting_price', response.data)

    def test_create_auction_invalid_starting_price_zero(self):
        """
        Test auction creation with an invalid starting price (e.g., negative value).
        """
        force_authenticate(self.client, user=self.user)
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': 0.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('starting_price', response.data)

    def test_create_auction_invalid_end_time(self):
        """
        Test auction creation with an invalid end time.
        """
        force_authenticate(self.client, user=self.user)
        end_time = timezone.now() - timezone.timedelta(days=1)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': 100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_time', response.data)

    def test_create_auction_unauthenticated(self):
        """
        Test auction creation without authentication.
        """
        self.client.credentials()  # Remove any existing authentication
        end_time = timezone.now() + timezone.timedelta(days=7)
        data = {
            'title': 'Test Auction',
            'description': 'This is a test auction.',
            'starting_price': 100.00,
            'end_time': end_time.isoformat(),
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuctionCancelViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.auction = Auction.objects.create(
            seller=self.user,
            title='Test Auction',
            description='This is a test auction.',
            starting_price=100.00,
            end_time=timezone.now() + timezone.timedelta(days=7),
            is_active=True,
        )
        self.auction_cancel_url = reverse(
            'auction_cancel', kwargs={'pk': self.auction.pk})

    def test_cancel_auction_success(self):
        """
        Test successful auction cancellation by the seller.
        """
        response = self.client.post(self.auction_cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auction.refresh_from_db()  # Refresh the auction object from the database
        self.assertFalse(self.auction.is_active)

    def test_cancel_auction_not_seller(self):
        """
        Test cancellation attempt by a user who is not the seller.
        """
        other_user = User.objects.create_user(
            username='otheruser', password='otherpassword')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')

        response = self.client.post(self.auction_cancel_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.auction.refresh_from_db()
        self.assertTrue(self.auction.is_active)

    def test_cancel_auction_already_ended(self):
        """
        Test cancellation of an auction that has already ended.
        """
        self.auction.end_time = timezone.now() - timezone.timedelta(days=1)
        self.auction.save()
        response = self.client.post(self.auction_cancel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.auction.refresh_from_db()
        self.assertTrue(self.auction.is_active)

    def test_cancel_auction_invalid_pk(self):
        """
        Test cancellation with an invalid auction primary key.
        """
        invalid_url = reverse(
            'auction_cancel', kwargs={'pk': 999})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_auction_unauthenticated(self):
        """
        Test cancellation without authentication.
        """
        self.client.credentials()  # Remove authentication
        response = self.client.post(self.auction_cancel_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.auction.refresh_from_db()
        self.assertTrue(self.auction.is_active)


class PlaceBidViewTests(APITestCase):
    def setUp(self):
        # Create a user (buyer)
        self.user = User.objects.create_user(
            username='buyer', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a seller
        self.seller = User.objects.create_user(
            username='seller', password='sellerpassword')
        self.seller_token = Token.objects.create(user=self.seller)

        # Create an auction owned by the seller
        self.auction = Auction.objects.create(
            seller=self.seller,
            title='Test Auction',
            description='This is a test auction.',
            starting_price=100.00,
            end_time=timezone.now() + timezone.timedelta(days=7),
            is_active=True,
        )

        # Create a bidder
        self.bidder = User.objects.create_user(
            username='bidder', password='bidderpassword')

        self.url = reverse(
            'place_bid', kwargs={'pk': self.auction.pk})

    def test_place_bid_success(self):
        """
        Test successful bid placement.
        """
        data = {'amount': 120.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bid.objects.count(), 1)
        bid = Bid.objects.first()
        self.assertEqual(bid.bidder, self.user)
        self.assertEqual(bid.auction, self.auction)
        self.assertEqual(bid.amount, 120.00)
        auction = Auction.objects.get(pk=self.auction.pk)
        self.assertEqual(auction.current_bid, 120.00)

    def test_place_bid_below_starting_price(self):
        """
        Test bid below the starting price.
        """
        data = {'amount': 90.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        self.assertEqual(
            response.data['amount'][0], 'Bid must be higher than the starting price.')

    def test_place_bid_below_current_highest(self):
        """
        Test bid below the current highest bid.
        """
        # Create a higher bid first
        Bid.objects.create(
            bidder=self.bidder,
            auction=self.auction,
            amount=150.00
        )
        data = {'amount': 140.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        self.assertEqual(
            response.data['amount'][0], 'Bid must be higher than the current highest bid.')

    def test_place_bid_outbid_self(self):
        """
        Test outbid user's own bid. (prohibit user from bidding consecutively)
        """
        # Create bid for the user
        Bid.objects.create(
            bidder=self.user,
            auction=self.auction,
            amount=150.00
        )
        data = {'amount': 160.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        self.assertEqual(
            response.data['amount'][0], 'You cannot outbid on yourself.')

    def test_place_bid_by_seller(self):
        """
        Test bid placement by the seller of the auction.
        """
        # Authenticate as seller
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.seller_token.key}')
        data = {'amount': 200.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_place_bid_on_ended_auction(self):
        """
        Test bid on an auction that has already ended.
        """
        self.auction.end_time = timezone.now() - timezone.timedelta(days=1)
        self.auction.save()
        data = {'amount': 120.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        self.assertEqual(response.data['amount'][0], 'Auction has ended.')

    def test_place_bid_invalid_auction_pk(self):
        """
        Test bid on an invalid auction pk.
        """
        invalid_url = reverse('place_bid', kwargs={'pk': 999})
        data = {'amount': 120.00}
        response = self.client.post(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_place_bid_unauthenticated(self):
        """
        Test bid without authentication.
        """
        self.client.credentials()
        data = {'amount': 120.00}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
