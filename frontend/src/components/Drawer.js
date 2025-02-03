import { useState, useEffect } from "react";

export default function Drawer({ isOpen, setMessages, setConvId }) {
    const [chatHistory, setChatHistory] = useState([]);

    useEffect(() => {
        try {
            const savedHistory = localStorage.getItem('chatHistory');
            if (savedHistory) {
                const parsedHistory = JSON.parse(savedHistory);
                // Ensure we're setting an array
                setChatHistory(Array.isArray(parsedHistory) ? parsedHistory : [parsedHistory]);
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
            setChatHistory([]);
        }
    }, [isOpen]);

    const loadChat = (history) => {
        setMessages(history.messages);
        setConvId(history.convId);
    };

    return (
        <div className={`fixed top-0 left-0 h-full w-80 bg-neutral-900/60 transform transition-transform duration-300 ease-in-out ${
            isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
            <h2 className="text-2xl font-normal text-white p-4 border-b border-gray-700 font-['Montserrat']">Chat History</h2>
            <ul className="menu p-4">
                {chatHistory.map((chat, index) => (
                        <li key={chat.convId}>
                            <button onClick={() => loadChat(chat)}>
                                Chat {index + 1} - {new Date(chat.timestamp).toLocaleDateString()}
                            </button>
                        </li>
                    ))}
            </ul>
        </div>
    );
}