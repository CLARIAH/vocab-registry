"""Module to define data models for rating reviews."""
import datetime
import unittest

from enum import StrEnum
from typing import List, Optional
from pydantic import BaseModel, Field


class AuthorModel(BaseModel):
    """Model representing the author of a review.

        Attributes:
            type_ (str): The type of the author. Default is 'Person'.
            name (str): The name of the author.
        """
    type_: str = Field(alias="@type", default='Person')
    name: str


class ReviewRatingModel(BaseModel):
    """Model representing a rating with reviews.

        Attributes:
            context (str): The context of the rating. Default is 'https://schema.org/'.
            type_ (str): The type of the rating. Default is 'Product'.
            reviews (List[ReviewModel]): List of reviews for the rating.
            aggregateRating (AggregateRatingModel): Aggregate rating for the rating.
        """
    type_: str = Field(alias="@type", default="rating")
    worstRating: int = Field(default=1)
    bestRating: int = Field(default=5)
    ratingValue: int


class InteractionTypeAction(StrEnum):
    """
       Enumeration for interaction types.
       """
    LIKE = 'LikeAction'
    DISLIKE = 'DislikeAction'


class InteractionStatisticItemModel(BaseModel):
    """
        Model representing an interaction statistic item.

        Attributes:
            type_ (str): The type of the interaction statistic item.
            interactionType (InteractionTypeAction): The type of interaction.
            author (AuthorModel): The author of the interaction.
        """
    interactionType: InteractionTypeAction
    author: AuthorModel
    delete: Optional[bool] = None


class ReviewModel(BaseModel):
    """Model representing the rating of a rating review.

        Attributes:
            type_ (str): The type of the rating. Default is 'rating'.
            worstRating (str): The worst possible rating. Default is '1'.
            bestRating (str): The best possible rating. Default is '5'.
            ratingValue (str): The actual rating value.
        """
    type_: str = Field(alias="@type", default="review")
    author: AuthorModel
    datePublished: str = Field(default=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    reviewBody: Optional[str] = None
    reviewRating: Optional[ReviewRatingModel] = None
    interactionStatistic: Optional[List[InteractionStatisticItemModel]] = None


class AggregateRatingModel(BaseModel):
    """Model representing aggregate rating information.

        Attributes:
            type_ (str): The type of the aggregate rating. Default is 'AggregateRating'.
            ratingValue (str): The value of the aggregate rating.
            bestRating (str): The highest possible rating value.
            ratingCount (str): The total number of ratings.
        """
    type_: str = Field(alias="@type", default='AggregateRating')
    ratingValue: float
    bestRating: int
    ratingCount: int


class RatingModel(BaseModel):
    """Model representing a rating with reviews.

        Attributes:
            context (str): The context of the rating. Default is 'https://schema.org/'.
            type_ (str): The type of the rating. Default is 'Product'.
            reviews (List[ReviewModel]): List of reviews for the rating.
            aggregateRating (AggregateRatingModel): Aggregate rating for the rating.
        """
    context: str = Field(alias="@context", default="https://schema.org/")
    type_: str = Field(alias="@type", default="Product")
    reviews: List[ReviewModel]
    aggregateRating: Optional[AggregateRatingModel] = None

class TestModels(unittest.TestCase):

    def test_AuthorModel(self):
        author_data = {"name": "Eko Indarto"}
        author = AuthorModel(**author_data)
        self.assertEqual(author.name, "Eko Indarto")
        self.assertEqual(author.type_, "Person")  # Default value

    def test_ReviewRatingModel(self):
        review_rating_data = {"ratingValue": 4}
        review_rating = ReviewRatingModel(**review_rating_data)
        self.assertEqual(review_rating.ratingValue, 4)
        self.assertEqual(review_rating.type_, "rating")  # Default value
        self.assertEqual(review_rating.worstRating, 1)  # Default value
        self.assertEqual(review_rating.bestRating, 5)  # Default value

    def test_ReviewModel(self):
        author_data = {"name": "Eko Indarto"}
        review_rating_data = {"ratingValue": 4}
        review_data = {
            "author": author_data,
            "reviewBody": "Great product!",
            "reviewRating": review_rating_data
        }
        review = ReviewModel(**review_data)
        self.assertEqual(review.reviewBody, "Great product!")
        self.assertEqual(review.author.name, "Eko Indarto")
        # self.assertEqual(review.datePublished[:4], str(datetime.utcnow().year))  # Check if year is correct
        self.assertEqual(review.type_, "review")  # Default value

    def test_AggregateRatingModel(self):
        aggregate_rating_data = {"ratingValue": 4, "bestRating": 5, "ratingCount": 100}
        aggregate_rating = AggregateRatingModel(**aggregate_rating_data)
        self.assertEqual(aggregate_rating.ratingValue, 4)
        self.assertEqual(aggregate_rating.ratingCount, 100)
        self.assertEqual(aggregate_rating.type_, "AggregateRating")  # Default value

    def test_InteractionStatisticItemModel(self):
        author_data = {"name": "Eko Indarto"}
        interaction_statistic_data = {"interactionType": InteractionTypeAction.LIKE, "author": author_data}
        interaction_statistic = InteractionStatisticItemModel(**interaction_statistic_data)
        self.assertEqual(interaction_statistic.interactionType, InteractionTypeAction.LIKE)
        self.assertEqual(interaction_statistic.author.name, "Eko Indarto")
        self.assertIsNone(interaction_statistic.type_)  # Type is required, but not specified in test data

    def test_RatingModel(self):
        author_data = {"name": "Eko Indarto"}
        review_rating_data = {"ratingValue": 4}
        review_data = {
            "author": author_data,
            "reviewBody": "Great product!",
            "reviewRating": review_rating_data
        }
        review = ReviewModel(**review_data)
        aggregate_rating_data = {"ratingValue": 4, "bestRating": 5, "ratingCount": 100}
        aggregate_rating = AggregateRatingModel(**aggregate_rating_data)
        interaction_statistic_data = [{"interactionType": InteractionTypeAction.LIKE, "author": author_data}]
        rating_data = {
            "reviews": [review],
            "aggregateRating": aggregate_rating,
            "interactionStatistic": interaction_statistic_data
        }
        rating = RatingModel(**rating_data)
        self.assertEqual(len(rating.reviews), 1)
        self.assertEqual(rating.aggregateRating.ratingValue, 4)
        self.assertEqual(len(rating.interactionStatistic), 1)


# Example usage:
json_data = """
{
  "@context": "https://schema.org/",
  "@type": "Review",
  "reviews": [
    {
      "@type": "review",
      "author": {
        "@type": "Person",
        "name": "Eko Indarto"
      },
      "datePublished": "2024-04-18 12:00:00",
      "reviewBody": "Great Review!",
      "reviewRating": {
        "@type": "rating",
        "worstRating": 1,
        "bestRating": 5,
        "ratingValue": 4
      }
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4,
    "bestRating": 5,
    "ratingCount": 1
  },
  "interactionStatistic": [
    {
      "@type": "LikeAction",
      "interactionType": "LikeAction",
      "author": {
        "@type": "Person",
        "name": "Wilko steinhoff"
      }
    },
    {
      "@type": "LikeAction",
      "interactionType": "LikeAction",
      "author": {
        "@type": "Person",
        "name": "Kerim Meijer"
      }
    },
     {
      "@type": "LikeAction",
      "interactionType": "DislikeAction",
      "author": {
        "@type": "Person",
        "name": "Daan Jansen"
      }
    },
    {
      "@type": "LikeAction",
      "interactionType": "LikeAction",
      "author": {
        "@type": "Person",
        "name": "Amal Khairunnisa"
      }
    },
    {
      "@type": "LikeAction",
      "interactionType": "LikeAction",
      "author": {
        "@type": "Person",
        "name": "Menzo Windhouwer"
      }
    },
     {
      "@type": "LikeAction",
      "interactionType": "DislikeAction",
      "author": {
        "@type": "Person",
        "name": "Kerim Meyer"
      }
    }
  ]
}

"""

