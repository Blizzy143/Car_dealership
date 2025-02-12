import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header/Header";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";

const Dealer = () => {
  const [dealer, setDealer] = useState(null); // ✅ Use `null` instead of `{}`
  const [loading, setLoading] = useState(true);
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  let { id } = useParams();
  let root_url = window.location.origin + "/djangoapp";
  let dealer_url = `${root_url}/get_dealer_details/${id}/`;
  let reviews_url = `${root_url}/get_dealer_reviews/${id}/`;
  let post_review = `${root_url}/postreview/${id}`;

  // ✅ Fetch dealer details
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();

      console.log("Dealer API Response:", retobj); // ✅ Debugging log

      if (retobj.status === 200 && retobj.dealer) {
        setDealer(retobj.dealer); // ✅ Use `retobj.dealer`, not `retobj.dealer[0]`
      } else {
        console.error("Dealer not found.");
        setDealer(null); // ✅ Prevents errors in rendering
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
    } finally {
      setLoading(false); // ✅ Stop loading message
    }
  };

  // ✅ Fetch reviews
  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url);
      const retobj = await res.json();

      if (retobj.status === 200 && retobj.reviews.length > 0) {
        setReviews(retobj.reviews);
      } else {
        setUnreviewed(true);
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  // ✅ Determine sentiment icon
  const senti_icon = (sentiment) => {
    return sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review}>
          <img
            src={review_icon}
            style={{ width: "10%", marginLeft: "10px", marginTop: "10px" }}
            alt="Post Review"
          />
        </a>
      );
    }
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <Header />

      {/* ✅ Handle loading state */}
      {loading ? (
        <h3 style={{ color: "red" }}>Loading dealer details...</h3>
      ) : dealer ? (
        <>
          <div style={{ marginTop: "10px" }}>
            <h1 style={{ color: "grey" }}>{dealer.full_name} {postReview}</h1>
            <h4 style={{ color: "grey" }}>
              {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
            </h4>
          </div>
        </>
      ) : (
        <h3 style={{ color: "red" }}>Dealer not found.</h3>
      )}

      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <p>Loading Reviews....</p>
        ) : unreviewed ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review) => (
            <div className="review_panel" key={review.id}>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;