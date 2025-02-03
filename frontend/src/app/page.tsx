"use client";

import Head from "next/head";
import TextInput from "../components/TextInput";
import NavBar from "../components/NavBar";
import Drawer from "../components/Drawer";
import ChatBox from '../components/ChatBox';
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "../config.js";

const Page = () => {
  const [userId, setUserId] = useState(null);
  const [convId, setConvId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  interface Message {
    type: 'user' | 'agent';
    content: string;
  }
  const [messages, setMessages] = useState<Message[]>([]);
  const mainContentRef = useRef<HTMLDivElement>(null);

  // upon initial mount (first time only), create user and conversation
  useEffect(() => {
    const initializeChat = async () => {
      try {
        // Create user
        const userResponse = await axios.post(API_ENDPOINTS.POST_CREATE_USER);
        if (userResponse.status !== 201) {
          console.error("Failed to create user");
          return;
        }
        const newUserId = userResponse.data.user_id;
        setUserId(newUserId);
        localStorage.setItem('userId', newUserId);

        // Create conversation
        const convResponse = await axios.post(
          API_ENDPOINTS.POST_CREATE_CONV,
          { user_id: newUserId }
        );
        if (convResponse.status !== 201) {
          console.error("Failed to create conversation");
          return;
        }
        const newConvId = convResponse.data.conv_id;
        setConvId(newConvId);
      } catch (error) {
        console.error("Error initializing chat:", error);
      }
    };
    initializeChat();
  }, []);

  // open and close drawer
  const handleDrawerToggle = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };

  // close drawer when clicking outside the drawer (CAREFUL)
  const handleClickOutside = (event: MouseEvent) => {
    if (
      isDrawerOpen && 
      mainContentRef.current && 
      event.target instanceof Node && // Type guard for event.target
      mainContentRef.current.contains(event.target)
    ) {
      setIsDrawerOpen(false);
    }
  };

  // if drawer is open, listen to mouse clicks outside the drawer
  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDrawerOpen]);


  const handleSendMessage = async () => {
    try {
        // Add user message
        setMessages((prev: Message[]) => [...prev, { type: 'user', content: inputValue }]);
        const userMessage = inputValue;
        setInputValue('');
        const url: string = API_ENDPOINTS.PUT_UPDATE_CONV.replace(':convId', convId as string);
        const response = await axios.put(`${url}`,
          { user_id: userId, message: userMessage }
        );
        if (response.status !== 200) {
          console.error("Failed to get message from agent.");
          return;
        }
        // Add LLM response
        setMessages((prev: Message[]) => [...prev, { type: 'agent', content: response.data.message }]);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

  return (
    <div 
      className="relative min-h-screen before:content-[''] before:absolute before:inset-0 before:bg-black/10"
      style={{
        backgroundImage: "url('/bg.jpeg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed'
      }}>
      <Drawer 
      isOpen={isDrawerOpen}
      setMessages={setMessages} 
      setConvId={setConvId} />
      <div 
        ref={mainContentRef}
        className={`min-h-screen transition-transform duration-300 ease-in-out ${
          isDrawerOpen ? 'translate-x-80' : 'translate-x-0'
        }`}
      >
        <NavBar 
          onMenuClick={handleDrawerToggle}
          setConvId={setConvId}
          setMessages={setMessages}
          convId={convId}
          messages={messages} />
        <div className="p-4">
          <Head>
            <title>Next.js + Tailwind CSS</title>
            <meta name="description" content="Next.js + Tailwind CSS" />
            <link rel="icon" href="/favicon.ico" />
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet" />
          </Head>
          <main className="text-center pt-16">
          <h1 className={"text-4xl font-normal text-ededed tracking-wide mb-6 font-['Montserrat']"}>
              Ask me anything about Yann LeCun!
            </h1>
            <div className="w-[47.2%] mx-auto h-[calc(100vh-300px)] mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm">
              <ChatBox messages={messages} />
            </div>
            <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 p-4 w-[60%] mb-4">
              <div className="relative flex items-center w-full">
                <TextInput 
                  content={inputValue} 
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInputValue(e.target.value)}
                  onKeyDown={(e: React.KeyboardEvent<HTMLTextAreaElement>) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                      setInputValue(''); 
                    }
                  }}
                  className="w-full min-h-[80px] pr-16 pl-4 py-2 text-zinc-200 rounded-lg border border-zinc-400/30 bg-zinc-800/10 focus:outline-none focus:border-zinc-400 shadow-2xl shadow-zinc-950/90 hover:shadow-2xl transition-shadow duration-300 backdrop-blur-sm placeholder:text-neutral-400"
                />
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Page;