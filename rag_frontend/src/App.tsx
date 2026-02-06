import { useState, useRef, useEffect } from 'react'


interface ChatMessage {
  role: 'user' | 'ai' ;
  text: string;
}

interface APIresponse{
  answer: string;
}

const App: React.FC = () => {

  const [input, setInput] = useState<string>("");
  const [chat, setChat] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({behavior:"smooth"})
  }

  useEffect(() => {
    scrollToBottom();
  },[chat, loading])

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput("");
    setLoading(true);

    const updatedChat: ChatMessage[] = [...chat, {role:'user', text: userQuery}]
    setChat(updatedChat)

    try{
      const response = await fetch("http://localhost:5001/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({message: userQuery})
      })
      if (!response.ok) throw new Error("Fel på server")
      const data: APIresponse = await response.json();

      setChat([...updatedChat, {role:'ai', text: data.answer}]);
    } catch(err){
      console.error("Fel: ", err);
      setChat([...updatedChat, {role:'ai', text:"Kunde inte hämta svar."}])
    } finally {
      setLoading(false);
    }
  };
  const TechBadge = ({ label }: { label: string }) => (
    <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs font-medium rounded-md border border-blue-100">
      {label}
    </span>
  );

  const InfoCard = () => (
    <div className="bg-gray-500 border border-gray-200 rounded-xl p-4 shadow-sm mb-6">
      <h2 className="text-sm font-bold text-gray-100 uppercase tracking-wider mb-3">
        Systemarkitektur
      </h2>
      <div className="flex flex-wrap gap-2">
        <TechBadge label="LangChain" />
        <TechBadge label="ChromaDB" />
        <TechBadge label="Flask API" />
        <TechBadge label="React + TS" />
        <TechBadge label="Tailwind v4" />
        <TechBadge label="Gemini API" />
      </div>
      <p className="mt-3 text-xs text-gray-100 leading-relaxed">
        RAG-assistent som hämtar kontext via semantisk sökning och genererar svar med Gemini 2.5/3.
      </p>
    </div>
  );


  return (
    <div className="flex flex-col h-screen bg-gray-400">
      {/* Header */}
      <header className="bg-gray-300 shadow-sm py-4 px-6 border-b border-gray-200">
        <InfoCard/>
        <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <span className="w-3 h-3 bg-green-500 rounded-full"></span>
          Gemini RAG Assistant
        </h1>
        <p>DEMO/POC VERSION</p>
        <p>PDF-material: Kapitel 1 och 2 av "Lär dig AI från grunden, Tillämpad maskinlärning med Python" av Prgomet, Johnsson, Solberg & Streuli</p>
      </header>

      {/* Chatfönster */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {chat.length === 0 && (
            <div className="text-center py-20 text-gray-400">
              <p className="text-lg italic">Ställ en fråga om dina dokument för att börja...</p>
            </div>
          )}

          {chat.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[85%] px-5 py-3 rounded-2xl shadow-sm ${msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                }`}>
                <p className="text-xs font-semibold uppercase tracking-wider mb-1 opacity-70">
                  {msg.role === 'user' ? 'Du' : 'Gemini'}
                </p>
                <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-500 px-5 py-3 rounded-2xl rounded-bl-none animate-pulse">
                Gemini skriver...
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      </main>

      {/* Inputfält */}
      <footer className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-3xl mx-auto flex gap-3">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all bg-gray-50"
            placeholder="Skriv din fråga här..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            Sök
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;