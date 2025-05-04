import { useEffect, useState } from 'react';
import useApi from '../Hooks/useApi';
import {
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
    if (active && payload?.length) {
        const { date, sentiment } = payload[0].payload;
        return (
            <div style={{ backgroundColor: "white", padding: "8px", border: "1px solid #ccc" }}>
                <p><strong>Date:</strong> {new Date(date).toLocaleDateString('en-US', {day: '2-digit', month: '2-digit', year: '2-digit'})}</p>
                <p><strong>Sentiment:</strong> {sentiment}</p>
            </div>
        );
    }

    return null;
};

const Graph = ({ selectedChannel }) => {
    const [messageData, setMessageData] = useState([]);

    const { getMessages } = useApi();
    
    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const data = await getMessages(selectedChannel);
                const transformedData = data.map((message) => ({
                    ...message,
                    date: new Date(message.created_at * 1000)
                }));
                setMessageData(transformedData);
            } catch {
                console.error("Error fetching messages");
            }
        };

        if (selectedChannel) fetchMessages();
    }, [selectedChannel]);

    const getAvgSentiment = () => {
        if (messageData.length === 0) return 0;
        const totalSentiment = messageData.reduce((acc, msg) => acc + msg.sentiment, 0);
        return (totalSentiment / messageData.length).toFixed(2);
    }

    const getNumMessages = () => {
        return messageData.length;
    }

    const getPercentPos = () => {
        if (messageData.length === 0) return 0;
        const numPos = messageData.filter(msg => msg.sentiment > 0.33).length;
        return ((numPos / messageData.length) * 100).toFixed(2);
    }
  
    return (
        <section className="flex-1 bg-white rounded-lg shadow-md p-4 min-h-[calc(100vh-116px)]">
            {selectedChannel && (
                <div className='w-full h-full'>
                    <h1 className="text-xl font-semibold mb-4">{selectedChannel}</h1>
                    <ResponsiveContainer width="100%" height={400}>
                        <ScatterChart>
                            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
                            <XAxis
                                dataKey="date"
                                scale="time"
                                type="number"
                                domain={['auto', 'auto']}
                                tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', {day: '2-digit', month: '2-digit', year: '2-digit'})}
                            />
                            <YAxis 
                                dataKey="sentiment"
                                type="number"
                                domain={[-1, 1]} 
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Scatter
                                name="Sentiment"
                                data={messageData.map(msg => ({ date: msg.date.getTime(), sentiment: msg.sentiment }))}
                                fill="#4f46e5"
                            />
                        </ScatterChart>
                    </ResponsiveContainer>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                        <div className="bg-highlight rounded-md p-4 shadow-sm">
                            <h2 className="text-sm font-medium">Average Sentiment</h2>
                            <p className="text-2xl font-bold">{getAvgSentiment()}</p>
                        </div>

                        <div className="bg-accent rounded-md p-4 shadow-sm">
                            <h2 className="text-sm font-medium">Number of Messages</h2>
                            <p className="text-2xl font-bold">{getNumMessages()}</p>
                        </div>

                        <div className="bg-highlight rounded-md p-4 shadow-sm">
                            <h2 className="text-sm font-medium">% Positive Messages</h2>
                            <p className="text-2xl font-bold">{getPercentPos()}%</p>
                        </div>
                    </div>
                </div>
            )}
        </section>
    );
};
  
export default Graph;