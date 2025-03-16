import React, { useRef } from "react";
import "./Home.css";
import { IoLogoTwitter, IoLogoGithub } from "react-icons/io";
import { Link } from "react-router-dom";
import Header from "./Header";
import creative from "../assets/creative.png";
import minimalist from "../assets/minimalist.png";
import professional from "../assets/professional.png";

function Home() {
  const scrollToRef = useRef(); // Fixed typo in 'scollToRef'
  
  const scrollFunc = () => {
    scrollToRef.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      <Header handleclick={scrollFunc} />

      <div className="heading">Resumaster</div>
      
      <div className="home-main">
        <div className="home-head">
          Get your developer-style resume ready with React Resume Builder
        </div>
        <div>All new platform to build a developer-style resume in just a few seconds.</div>

        <div className="img-home">
          <img src={creative} alt="Creative Resume Template" />
          <img src={minimalist} alt="Minimalist Resume Template" />
          <img src={professional} alt="Professional Resume Template" />
        </div>

        <div className="steps" ref={scrollToRef}> {/* Added ref here */}
          <div>Follow the steps</div>

          <div>
            <div className="step-head">Step 1:</div>
            <div className="step-subhead">Input all your details</div>
            <div className="step-subhead">Select the template you want</div>

            <div className="step-head">Step 2:</div>
            <div className="step-subhead">Customize your details</div>

            <div className="step-head">Step 3:</div>
            <div className="step-subhead">Your resume is ready to download</div>
            <div className="step-subhead">Click on download</div>

            <div className="step-head">Step 4:</div>
            <div className="step-subhead">You're done! 🎉</div>
          </div>
        </div>

        <div className="started">
          <div className="home-subheading">Are you ready?</div>
          <Link to={"/resumebuild"} className="link">
            <button className="started-btn">Get started</button>
          </Link>
        </div>
      </div>
    </>
  );
}

export default Home;
