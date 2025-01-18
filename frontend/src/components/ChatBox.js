import { useEffect, useRef } from 'react';

export default function ChatBox({ messages }) {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    return (
        <div className="w-[95%] h-full mx-auto overflow-y-auto mb-4">
            <div className="flex flex-col space-y-4 p-4">
                {messages.map((message, index) => (
                    <div 
                        key={index}
                        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div 
                            className={`max-w-[70%] px-4 py-2 rounded-lg ${
                                message.type === 'user' 
                                    ? 'bg-stone-700/10 text-white ml-auto shadow-md shadow-stone-900 text-left' 
                                    : 'bg-amber-700/10 text-white shadow-md shadow-stone-900 text-left'
                            }`}
                        >
                            {message.content}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
}