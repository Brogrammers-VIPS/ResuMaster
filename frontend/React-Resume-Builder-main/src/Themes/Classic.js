import React, { useState, useEffect } from 'react';
import './Classic.css';
import { IoMdMail } from 'react-icons/io';
import { BiMobileAlt, BiSquare } from 'react-icons/bi';
import { GrLinkedinOption } from 'react-icons/gr';
import { AiFillGithub } from 'react-icons/ai';
import { MdLocationOn } from 'react-icons/md';
import BounceLoader from 'react-spinners/BounceLoader';
import { useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

function Classic() {
    const themeclr = useSelector(state => state.theme?.theme?.color) || "#643baa";
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const userdata = useSelector(state => state.user.userdata);
    const [loadhint, setLoadHint] = useState("");

    const loadFunc = () => {
        const hints = [
            "Please wait, your resume is in process...",
            "Hint: Entering complete details will make your resume look awesome!"
        ];

        setLoading(true);

        hints.forEach((item, index) => {
            setTimeout(() => {
                setLoadHint(item);
            }, 3000 * index);
        });

        setTimeout(() => {
            setLoading(false);
        }, 6000);
    };

    useEffect(() => {
        if (!userdata.personal) {
            navigate("/");
        }
        window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
        loadFunc();
        // eslint-disable-next-line
    }, []);

    return (
        <>
            {loading ? (
                <>
                    <BounceLoader className="loader" color="#643baa" size={150} />
                    <div className="loader-hint mt-2 font-bold">{loadhint}</div>
                </>
            ) : (
                <div>
                    <div className="noprint">
                        <Link to="/resumebuild">
                            <button className="print-btn">Edit Data</button>
                        </Link>
                        <Link to="/selecttheme">
                            <button className="print-btn">Change Theme</button>
                        </Link>
                        <button className="print-btn" onClick={() => window.print()}>
                            Download
                        </button>
                    </div>

                    <div className="theme2">
                        <div className="mb-4">
                            <div>
                                <div className="text-3xl" style={{ color: themeclr, fontWeight: "bold" }}>
                                    {userdata.personal.name} {userdata.personal.lastname}
                                </div>
                                <div style={{ color: themeclr, fontSize: "19px" }}>
                                    {userdata.personal.title}
                                </div>
                            </div>
                            <div>
                                <div>{userdata.personal.email}</div>
                                <IoMdMail style={{ color: themeclr }} />
                                <div>{userdata.personal.mob}</div>
                                <BiMobileAlt style={{ color: themeclr }} />
                                <div>
                                    {userdata.personal.city}, {userdata.personal.country}
                                </div>
                                <MdLocationOn style={{ color: themeclr }} />
                                <div>{userdata.link.linkedin}</div>
                                <GrLinkedinOption style={{ color: themeclr }} />
                                <div>{userdata.link.github}</div>
                                <AiFillGithub style={{ color: themeclr }} />
                            </div>
                        </div>

                        {userdata.skills && userdata.skills.length > 0 && (
                            <div className="theme2-section">
                                <div className="section-head" style={{ color: themeclr }}>SKILLS</div>
                                <div className="section-content">
                                    <div className="theme2-interest">
                                        {userdata.skills.map((skill, index) => (
                                            <div
                                                key={index}
                                                style={{
                                                    backgroundColor: themeclr,
                                                    borderRadius: "5px",
                                                    padding: "3px",
                                                    fontSize: "12px"
                                                }}
                                            >
                                                {skill}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}

                        {userdata.experience.length > 0 && userdata.experience[0].company && (
                            <div className="theme2-section">
                                <div className="section-head" style={{ color: themeclr }}>WORK EXPERIENCE</div>
                                <div className="section-content">
                                    {userdata.experience.map((item, index) => (
                                        <div key={index}>
                                            <div className="font-bold" style={{ fontSize: "14px" }}>
                                                {item.title}
                                            </div>
                                            <div style={{ fontSize: "14px" }}>{item.company}</div>
                                            <div className="text-xs italic" style={{ color: themeclr }}>
                                                {item.starts_at} - {item.ends_at || "Present"}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}


                        {userdata.projects.length > 0 && (
                            <div className="theme2-section">
                                <div className="section-head" style={{ color: themeclr }}>PROJECTS</div>
                                <div className="section-content">
                                    {userdata.projects.map((item, index) => (
                                        <div key={index} className="theme2-proj">
                                            <BiSquare style={{ color: themeclr }} />
                                            <div>
                                                <div className="resume-title" style={{ fontWeight: "bold" }}>
                                                    {item.name}
                                                </div>
                                                <div className="text-xs" style={{ color: themeclr }}>
                                                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                                                        {item.url}
                                                    </a>
                                                </div>
                                                {item.description && <div className="mt-1">{item.description}</div>}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {userdata.education.length > 0 && (
                            <div className="theme2-section">
                                <div className="section-head" style={{ color: themeclr }}>EDUCATION</div>
                                <div className="section-content">
                                    {userdata.education.map((item, index) => (
                                        <div key={index} className="theme2-edu">
                                            
                                            <div className="resume-title">{item.school}</div>
                                            <div className="text-xs italic" style={{ color: themeclr }}>
                                                {item.starts_at} - {item.ends_at || "Present"}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </>
    );
}

export default Classic;
