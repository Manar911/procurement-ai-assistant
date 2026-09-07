import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";


const suggestions = [
  {
    label: "Top spending",
    question: "What are the top 5 departments by total spending?",
  },
  {
    label: "Supplier analysis",
    question: "Which suppliers received the most spending?",
  },
  {
    label: "Acquisition insights",
    question: "What is total spending by acquisition type?",
  },
  {
    label: "Purchase orders",
    question: "How many purchase orders were created in January 2014?",
  },
];


function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const messagesEndRef = useRef(null);


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);


  const sendQuestion = async (questionToSend) => {
    const trimmedQuestion = questionToSend.trim();

    if (!trimmedQuestion || isLoading) {
      return;
    }

    setError("");

    const userMessage = {
      role: "user",
      text: trimmedQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setQuestion("");
    setIsLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );


      if (!response.ok) {
        let errorMessage =
          "The assistant could not answer the question.";

        try {
          const errorData = await response.json();

          if (errorData.detail) {
            errorMessage = errorData.detail;
          }
        } catch {
          // Keep the default error message
        }

        throw new Error(errorMessage);
      }


      const data = await response.json();

      const assistantMessage = {
        role: "assistant",
        text: data.answer,
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);
    } catch (requestError) {
      console.error(requestError);

      setError(
        requestError.message ||
          "Something went wrong while contacting the assistant."
      );
    } finally {
      setIsLoading(false);
    }
  };


  const handleSubmit = () => {
    sendQuestion(question);
  };


  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSubmit();
    }
  };


  const handleSuggestionClick = (suggestionQuestion) => {
    sendQuestion(suggestionQuestion);
  };


  const handleNewConversation = () => {
    setMessages([]);
    setQuestion("");
    setError("");
  };


  const hasMessages = messages.length > 0;


  return (
    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            P
          </div>

          <div>
            <h1>ProcureAI</h1>

            <p>
              Procurement Intelligence
            </p>
          </div>
        </div>


        <button
          className="new-chat-button"
          onClick={handleNewConversation}
        >
          + New conversation
        </button>


        <div className="sidebar-section">

          <span className="sidebar-label">
            Workspace
          </span>

          <button className="sidebar-item active">
            Assistant
          </button>

        </div>


        <div className="sidebar-footer">

          <div className="status-dot" />

          <div>
            <strong>
              System ready
            </strong>

            <span>
              Connected to procurement data
            </span>
          </div>

        </div>

      </aside>


      <main className="main-content">

        <header className="topbar">

          <div>

            <span className="eyebrow">
              PROCUREMENT ASSISTANT
            </span>

            <h2>
              Ask your procurement data.
            </h2>

          </div>


          <div className="connection-badge">

            <span className="connection-dot" />

            Connected

          </div>

        </header>


        <section className="chat-area">

          {!hasMessages && (
            <>

              <div className="hero">

                <div className="hero-icon">
                  ✦
                </div>


                <h3>
                  Procurement intelligence,
                  without the query language.
                </h3>


                <p>
                  Ask questions about spending,
                  suppliers, departments, purchase
                  orders, and procurement trends
                  using natural language.
                </p>

              </div>


              <div className="suggestions">

                {suggestions.map((suggestion) => (
                  <button
                    key={suggestion.label}
                    onClick={() =>
                      handleSuggestionClick(
                        suggestion.question
                      )
                    }
                    disabled={isLoading}
                  >

                    <span>
                      {suggestion.label}
                    </span>

                    {suggestion.question}

                  </button>
                ))}

              </div>

            </>
          )}


          {hasMessages && (

            <div className="messages">

              {messages.map((message, index) => (

                <div
                  key={`${message.role}-${index}`}
                  className={`message-row ${message.role}`}
                >

                  <div className="message-role">

                    {message.role === "user"
                      ? "You"
                      : "ProcureAI"}

                  </div>


                  <div className="message-bubble">

                    {message.role === "assistant" ? (

                      <ReactMarkdown>
                        {message.text}
                      </ReactMarkdown>

                    ) : (

                      message.text

                    )}

                  </div>

                </div>
              ))}


              {isLoading && (

                <div className="message-row assistant">

                  <div className="message-role">
                    ProcureAI
                  </div>


                  <div className="message-bubble loading-message">

                    Analyzing procurement data...

                  </div>

                </div>

              )}


              <div ref={messagesEndRef} />

            </div>
          )}


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <div className="composer-wrapper">

            <div className="composer">

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask a procurement question..."
                rows="1"
                disabled={isLoading}
              />


              <button
                className="send-button"
                onClick={handleSubmit}
                disabled={
                  isLoading ||
                  !question.trim()
                }
              >

                {isLoading ? "…" : "↑"}

              </button>

            </div>


            <p className="composer-note">

              ProcureAI answers using the
              procurement dataset.

            </p>

          </div>

        </section>

      </main>

    </div>
  );
}


export default App;