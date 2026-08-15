import { useState } from "react";
import "./App.css";

const suggestedQuestions = [
  "What is supervised learning?",
  "Explain neural networks",
  "What is overfitting?",
  "Explain classification",
];

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    const question = input.trim();

    if (!question || isLoading) return;

    // Add user's message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get a response from the server.");
      }

      const data = await response.json();

      // Add real RAG response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the RAG server. Please make sure the backend is running.",
          sources: [],
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  const handleSuggestion = (question) => {
    setInput(question);
  };

  const startNewChat = () => {
    setMessages([]);
    setInput("");
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="logo">
          <div className="logo-icon">R</div>
          <span>RAGify</span>
        </div>

        <button className="new-chat" onClick={startNewChat}>
          <span>＋</span>
          New Chat
        </button>

        <div className="sidebar-section">
          <p className="section-title">RECENT CHATS</p>

          <button className="chat-item active">
            <span>💬</span>
            Machine Learning
          </button>

          <button className="chat-item">
            <span>💬</span>
            Neural Networks
          </button>

          <button className="chat-item">
            <span>💬</span>
            Classification
          </button>
        </div>

        <div className="sidebar-bottom">

          <button className="bottom-item">
            <span>⚙️</span>
            Settings
          </button>

          <button className="bottom-item">
            <span>❓</span>
            Help
          </button>

        </div>
      </aside>

      {/* Main */}
      <main className="main">

        {/* Top bar */}
        <header className="topbar">

          <div>
            <h2>Machine Learning</h2>
            <p>Ask questions about your document</p>
          </div>

          <button className="theme-button">
            ☀️
          </button>

        </header>

        {/* Chat area */}
        <section className="chat-area">

          {messages.length === 0 ? (

            /* Welcome screen */
            <div className="welcome">

              <div className="welcome-icon">
                ✦
              </div>

              <h1>
                What would you like to know?
              </h1>

              <p>
                Ask RAGify anything about your uploaded document.
              </p>

              <div className="suggestions">

                {suggestedQuestions.map((question) => (
                  <button
                    key={question}
                    onClick={() => handleSuggestion(question)}
                  >
                    {question}
                  </button>
                ))}

              </div>

            </div>

          ) : (

            /* Messages */
            <div className="messages">

              {messages.map((message, index) => (

                <div
                  key={index}
                  className={`message-row ${message.role}`}
                >

                  {/* Avatar */}
                  <div className="message-avatar">
                    {message.role === "user" ? "You" : "R"}
                  </div>

                  {/* Message */}
                  <div className="message-content">

                    <div>
                      {message.content}
                    </div>

                    {/* Sources */}
                    {message.role === "assistant" &&
                      message.sources &&
                      message.sources.length > 0 && (

                        <div className="sources">

                          <div className="sources-title">
                            Sources
                          </div>

                          {message.sources.map(
                            (source, sourceIndex) => (

                              <div
                                className="source-item"
                                key={sourceIndex}
                              >

                                <span>📄</span>

                                <div>

                                  <strong>
                                    {source.page
                                      ? `Page ${source.page}`
                                      : "Document"}
                                  </strong>

                                  <p>
                                    {source.content}
                                  </p>

                                </div>

                              </div>

                            )
                          )}

                        </div>

                      )}

                  </div>

                </div>

              ))}

              {/* Loading indicator */}
              {isLoading && (

                <div className="message-row assistant">

                  <div className="message-avatar">
                    R
                  </div>

                  <div className="message-content loading-message">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>

        {/* Input */}
        <div className="input-wrapper">

          <div className="input-box">

            <input
              type="text"
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about your document..."
            />

            <button
              className="send-button"
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
            >
              ➤
            </button>

          </div>

          <p className="input-note">
            RAGify answers questions using information from your document.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;