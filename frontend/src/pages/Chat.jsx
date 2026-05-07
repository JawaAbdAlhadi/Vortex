import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../css/Chat.css';
function Chat() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [newMessage, setNewMessage] = useState('');
  
  const [messages, setMessages] = useState([
    { id: 1, text: 'مرحباً، هل هذا المنتج لا يزال متوفراً؟', isMine: true },
    { id: 2, text: 'أهلاً بك، نعم متوفر وبحالة ممتازة.', isMine: false }
  ]);

  const handleSend = () => {
    if (!newMessage.trim()) return;
    setMessages([...messages, { id: Date.now(), text: newMessage, isMine: true }]);
    setNewMessage('');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#120A21] p-6">
      <div className="flex items-center mb-6">
        <button onClick={() => navigate(-1)} className="text-white text-2xl mr-4">
          &#8594;
        </button>
        <h1 className="text-xl font-bold text-white">المحادثة</h1>
      </div>

      <div className="flex-1 overflow-y-auto mb-4 flex flex-col gap-4">
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`p-3 max-w-[80%] ${
              msg.isMine 
                ? 'self-start bg-transparent border border-purple-500 rounded-2xl rounded-tr-none text-white' 
                : 'self-end bg-transparent border border-gray-500 rounded-2xl rounded-tl-none text-white text-right'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2 mt-auto">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          className="flex-1 bg-transparent border border-purple-500 rounded-full py-3 px-4 text-white focus:outline-none focus:ring-2 focus:ring-purple-400"
        />
        <button 
          onClick={handleSend}
          className="bg-[#5B39A0] px-6 py-3 rounded-full text-white font-bold"
        >
          إرسال
        </button>
      </div>
    </div>
  );
}

export default Chat;