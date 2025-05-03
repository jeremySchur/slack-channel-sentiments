import { useState, useEffect } from 'react';
import useApi from '../Hooks/useApi';
import SearchAndFilter from './SearchAndFilter';

const Channels = ({selectedChannel, setSelectedChannel}) => {
    const [channelList, setChannelList] = useState([]);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [sortOrder, setSortOrder] = useState("desc");

    const { getChannels } = useApi();

    useEffect(() => {
        const fetchChannels = async () => {
            try {
                const data = await getChannels();
                data.sort((a, b) => b.avg_sentiment - a.avg_sentiment);
                setChannelList(data);
            } catch {
                setError("Error fetching channels");
            }
        };

        fetchChannels();
    }, []);

    const handleClick = (index) => {
        setSelectedChannel(index);
        if (window.innerWidth < 1280) {
            document.getElementById("back_to_top").scrollIntoView({ behavior: "smooth", block: "start" });
        }
    };

    const filteredChannelList = [...channelList]
        .filter(channel => channel.name.toLowerCase().includes(searchQuery.toLowerCase()))
        .sort((a, b) => {
            const sentimentA = a.avg_sentiment;
            const sentimentB = b.avg_sentiment;

            if (sentimentA === undefined || sentimentA === null) return 1;
            if (sentimentB === undefined || sentimentB === null) return -1;

            return sortOrder === "desc"
                ? sentimentB - sentimentA  
                : sentimentA - sentimentB; 
    });

    const channelListItems = filteredChannelList.map((channel, index) => {
        return (
            <button
                key={index}
                className={`w-full flex justify-between items-center p-4 border-b border-gray-200 ${selectedChannel === index ? 'bg-highlight' : 'cursor-pointer'}`}
                onClick={() => handleClick(index)}
            >
                <p>{channel.name}</p>
                <p>{channel.avg_sentiment ? channel.avg_sentiment : "No data"}</p>
            </button>
        );
    });

    return (
        <section className="xl:w-1/3 h-[calc(100vh-116px)] bg-white rounded-lg shadow-md flex flex-col">
            <SearchAndFilter 
                searchQuery={searchQuery} 
                setSearchQuery={(query) => setSearchQuery(query)}
                sortOrder={sortOrder}
                setSortOrder={(order) => setSortOrder(order)}
            />

            <div className="flex justify-between p-4 border-b border-gray-200">
                <p className="text-lg text-left font-semibold">Channel Name</p>
                <p className="text-lg text-right font-semibold">Channel Sentiment</p>
            </div>

            <div className="overflow-y-auto scroll-container">
                {error ?
                    <p className="text-center mt-4">{error}</p> :
                    channelListItems.length > 0 ?
                        channelListItems :
                        <p className="text-center mt-4">No data available</p>
                }
            </div>
        </section>
    );
};

export default Channels;