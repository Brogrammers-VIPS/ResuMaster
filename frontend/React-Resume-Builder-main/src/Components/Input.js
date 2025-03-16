import React, { useEffect, useState } from "react";
import "./Input.css";
import { useForm } from "react-hook-form";
import { useDispatch, useSelector } from "react-redux";
import { clruserdata, getuserdata } from "../Redux/Reducers/userReducer";
import { useNavigate } from "react-router-dom";
import BounceLoader from 'react-spinners/BounceLoader'

function Input() {
    const [loading, setLoading] = useState(true);
    const [fetchingRepos, setFetchingRepos] = useState(false);
    const [githubRepos, setGithubRepos] = useState([]);
    const [selectedProjects, setSelectedProjects] = useState([]);
    const [githubUsername, setGithubUsername] = useState("");
    const [fetchError, setFetchError] = useState("");
    
    const userredux = useSelector(state => state.user.userdata)
    const dispatch = useDispatch()
    const navigate = useNavigate()
    
    const emptydata = {
        experience: [{
            company: "", description: "", worktitle: "",tags:"", yearfrom: "", yearto: "", present: false
        }],
        course: [{
            name: "", provider: ""
        }],
        education: [{
            degree: "", grade: "", university: "", yearfrom: "", yearto: "", gradetype: "percentage"
        }],
        personal: {
            technicalskill: [{
                skill: "", rate: ""
            }],
            interest: [{
                hobbie: ""
            }],
            name: "", lastname: "", date: "", email: "", mob: "",
            city: "", country: "", image: "",
            title: "", quote: ""
        },
        project: [],
        link: {
            linkedin: "",
            github: "",
            portfolio: ""
        },
    }
    
    const filldata = userredux.personal ? userredux : emptydata

    const { register, handleSubmit, formState: { errors }, reset, watch, setValue } = useForm(
        {
            defaultValues: filldata
        }
    );

    // Watch the GitHub URL to extract username
    const githubUrl = watch("link.github");

    useEffect(() => {
        // Extract GitHub username from URL
        if (githubUrl) {
            const match = githubUrl.match(/github\.com\/([^\/]+)/);
            if (match && match[1]) {
                setGithubUsername(match[1]);
            }
        }
    }, [githubUrl]);

    const loadFunc = () => {
        setLoading(true)
        setTimeout(() => {
            setLoading(false)
        }, 1000)
    }

    useEffect(() => {
        window.scrollTo({
            top: 0, left: 0, behavior: "smooth"
        })
        loadFunc()
        // eslint-disable-next-line
    }, [])

    const fetchGithubProjects = async () => {
        if (!githubUsername) {
            setFetchError("Please enter a valid GitHub URL first");
            return;
        }
        
        setFetchingRepos(true);
        setFetchError("");
        
        try {
            const response = await fetch(`https://api.github.com/users/${githubUsername}/repos?sort=updated&per_page=100`);
            
            if (!response.ok) {
                throw new Error("Failed to fetch repositories. Please check the GitHub username.");
            }
            
            const data = await response.json();
            setGithubRepos(data.map(repo => ({
                id: repo.id,
                name: repo.name,
                description: repo.description || "No description available",
                tech: repo.language || "",
                link: repo.html_url
            })));
            
        } catch (error) {
            setFetchError(error.message);
        } finally {
            setFetchingRepos(false);
        }
    };

    const toggleProjectSelection = (repo) => {
        if (selectedProjects.some(project => project.id === repo.id)) {
            // If already selected, remove it
            setSelectedProjects(selectedProjects.filter(project => project.id !== repo.id));
        } else if (selectedProjects.length < 3) {
            // If not selected and less than 3 projects selected, add it
            setSelectedProjects([...selectedProjects, repo]);
        }
    };

    const onSubmit = (data) => {
        // Add selected projects to form data
        const formData = {
            ...data,
            project: selectedProjects
        };
        
        dispatch(getuserdata(formData));
        navigate("/selecttheme");
    }

    const clrFunc = () => {
        setGithubRepos([]);
        setSelectedProjects([]);
        setGithubUsername("");
        dispatch(clruserdata());
        reset(emptydata);
    }

    return (
        <>
            {loading ? <BounceLoader className='loader' color="#643baa" size={150} /> :
                <>
                   <div className="input-header">Enter your details</div>
                    <div className="input-main">
                        <form className="input-form" onSubmit={handleSubmit(onSubmit)}>

                            <div className="input-head">Personal Details</div>
                            <input  {...register("personal.name", { required: true })} placeholder="Name" />
                            <input className="input-mob singlefield" type={"number"} inputMode={"tel"} {...register("personal.mob", { maxLength: 10, required: true })} placeholder="Mobile No- +91" />
                            <input className="singlefield" type={"email"} inputMode={"email"} {...register("personal.email", { required: true })} placeholder="Email" />
                            
                            <div className="github-input-container">
                                <input 
                                    className="github-input" 
                                    {...register("link.github", { required: true })} 
                                    placeholder="Github Url (e.g. https://github.com/username)" 
                                />
                                <button 
                                    type="button" 
                                    className="fetch-btn" 
                                    onClick={fetchGithubProjects}
                                    disabled={fetchingRepos || !githubUsername}
                                >
                                    {fetchingRepos ? "Fetching..." : "Fetch Projects"}
                                </button>
                            </div>
                            
                            {fetchError && <div className="fetch-error">{fetchError}</div>}
                            
                            {githubRepos.length > 0 && (
                                <div className="project-selection-container singlefield">
                                    <div className="project-selection-header">
                                        <h4>Select up to 3 projects</h4>
                                        <span>Selected: {selectedProjects.length}/3</span>
                                    </div>
                                    <div className="repo-list">
                                        {githubRepos.map(repo => (
                                            <div 
                                                key={repo.id} 
                                                className={`repo-item ${selectedProjects.some(p => p.id === repo.id) ? 'selected' : ''}`}
                                                onClick={() => toggleProjectSelection(repo)}
                                            >
                                                <div className="repo-name">{repo.name}</div>
                                                <div className="repo-description">{repo.description}</div>
                                                {repo.tech && <div className="repo-tech">Tech: {repo.tech}</div>}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                            
                            <input className="singlefield" {...register("link.linkedin", { required: true })} placeholder="LinkedIn Url" />

                            {errors.personal || errors.link ?
                                <span className="input-err singlefield">Please enter the required field</span> : null}
                            {userredux.personal ? <div className="singlefield btndiv mt-3">
                                <input className="input-btn" value={"Clear All"} onClick={clrFunc} />
                                <input className="input-btn" type="submit" value={"Next"} />
                            </div> :
                                <input className="input-btn singlefield mt-3" type="submit" value={"Next"} />}
                        </form>
                    </div>
                </>}
        </>
    );
}

export default Input;