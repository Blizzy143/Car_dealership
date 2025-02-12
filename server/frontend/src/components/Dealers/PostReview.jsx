import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let params = useParams();
  let id = params.id;

  let dealer_url = `${root_url}/get_dealer_details/${id}/`;  // ✅ FIXED URL
  let review_url = `${root_url}/add_review`;
  let carmodels_url = `${root_url}/get_cars`;

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (!sessionStorage.getItem("firstname") || !sessionStorage.getItem("lastname")) {
      name = sessionStorage.getItem("username");
    }

    // ✅ Form Validation
    if (!model || !review.trim() || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    let [make_chosen, model_chosen] = model.split(" ");
    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });

    console.log("Review JSON:", jsoninput);
    
    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsoninput,
      });

      const json = await res.json();
      if (json.status === 200) {
        window.location.href = window.location.origin + "/dealer/" + id;
      } else {
        alert("Failed to submit review. Try again.");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("Network error. Please try again.");
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();

      if (retobj.status === 200) {
        let dealerobjs = Array.from(retobj.dealer);
        if (dealerobjs.length > 0) setDealer(dealerobjs[0]);
      }
    } catch (error) {
      console.error("Error fetching dealer details:", error);
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url);
      const retobj = await res.json();

      setCarmodels(retobj.CarModels || []);
    } catch (error) {
      console.error("Error fetching car models:", error);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        
        <textarea
          id="review"
          cols="50"
          rows="7"
          placeholder="Write your review..."
          onChange={(e) => setReview(e.target.value)}
        />

        <div className="input_field">
          <label>Purchase Date</label>
          <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className="input_field">
          <label>Car Make & Model</label>
          <select onChange={(e) => setModel(e.target.value)}>
            <option value="" disabled hidden>Choose Car Make and Model</option>
            {carmodels.map((carmodel, index) => (
              <option key={index} value={`${carmodel.CarMake} ${carmodel.CarModel}`}>
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          <label>Car Year</label>
          <input type="number" max={2023} min={2015} onChange={(e) => setYear(e.target.value)} />
        </div>

        <button className="postreview" onClick={postreview}>Post Review</button>
      </div>
    </div>
  );
};

export default PostReview;