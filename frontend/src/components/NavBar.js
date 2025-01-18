import Modal from './Modal';

export default function NavBar({ onMenuClick }) {

    const handleViewMemory = () => {
        document.getElementById('my_modal_3').showModal();
    };

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
                <span className="text-xl font-normal font-['Montserrat']">RAG App</span>
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
                        <li><a>Upload to Memory</a></li>
                        <li><a onClick={handleViewMemory}>View Memory</a></li>
                    </ul>
                    <Modal />
                </div>
            </div>
        </div>
    );
}