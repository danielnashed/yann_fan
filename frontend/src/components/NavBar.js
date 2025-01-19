import Modal from './Modal';
import axios from 'axios';
import { API_ENDPOINTS } from "../config.js";

export default function NavBar({ onMenuClick, setConvId, setMessages, convId, messages }) {

    const handleViewMemory = () => {
        document.getElementById('my_modal_3').showModal();
    };

    const handleNewChat = async () => {
        
        const userId = localStorage.getItem('userId');

        // Save current chat before creating new one
        const History = {
            convId,
            messages,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('chatHistory', JSON.stringify(History));

        // Create new conversation
        const convResponse = await axios.post(
            API_ENDPOINTS.POST_CREATE_CONV,
            { user_id: userId }
            );
        if (convResponse.status !== 201) {
        console.error("Failed to create conversation");
        return;
        }
        const newConvId = convResponse.data.conv_id;
        setConvId(newConvId); // Update parent state
        setMessages([]); // Clear messages
    }

    return (
        <div className="navbar bg-base-100 bg-zinc-800/0 fixed top-0 w-full z-50">
            <div className="flex-none">
                <button onClick={onMenuClick} className="btn btn-square btn-ghost">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block h-5 w-5 stroke-current">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
            <div className="flex-1">
                <span className="text-xl font-normal font-['Montserrat']">Yann Fan RAG App</span>
            </div>
            <div className="flex-none">
                <div className="dropdown dropdown-left dropdown-hover">
                    <button tabIndex={0} className="btn btn-square btn-ghost">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            className="inline-block h-5 w-5 stroke-current">
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z">
                            </path>
                        </svg>
                    </button>
                    <ul tabIndex={0} className="dropdown-content menu bg-zinc-900/70 rounded-box z-[1] w-52 p-2 shadow-zinc-800 shadow-lg bg-blend-darken">
                        {/* <li><a>Examples</a></li> */}
                        <li><a onClick={handleNewChat}>New Chat</a></li>
                        <li><a onClick={handleViewMemory}>Memory</a></li>
                    </ul>
                    <Modal />
                </div>
            </div>
        </div>
    );
}