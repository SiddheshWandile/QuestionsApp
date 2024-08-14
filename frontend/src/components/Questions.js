import React, { useState } from "react";
import axios from "axios";
import "./Login.css";

const Questions = () => {
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [sourceCode, setSourceCode] = useState("");
  const [error, setError] = useState("");

  const questions = [
    { id: 1, text: "Binary Search Algorithm" },
    { id: 2, text: "Fibonacci Series" },
    { id: 3, text: "Bubble Sort" },
    { id: 4, text: "Merge Sort" },
    { id: 5, text: "Quick Sort" },
  ];

  const handleSubmit = async () => {
    if (!selectedQuestion) {
      setError("Please select a question.");
      return;
    }
  
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/question", {
        question_no: selectedQuestion.id,         
      });
      console.log(selectedQuestion.id);
  
      setSourceCode(response.data.source_code);  
      setError("");
    } catch (err) {
      setError("An error occurred while fetching the source code.");
    }
  };
  

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-8 form">
          <div className="view">
            <h2>Select a Question</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <ul className="list-group">
              {questions.map((question) => (
                <li
                  key={question.id}
                  className={`list-group-item ${selectedQuestion?.id === question.id ? "active" : ""}`}
                  onClick={() => setSelectedQuestion(question)}
                >
                  {question.text}
                </li>
              ))}
            </ul>
            <button
              type="button"
              className="btn btn-primary mt-3"
              onClick={handleSubmit}
            >
              Submit
            </button>
            {sourceCode && (
              <div className="mt-4">
                <h3>Source Code:</h3>
                <pre className="bg-light p-3">{sourceCode}</pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Questions;
