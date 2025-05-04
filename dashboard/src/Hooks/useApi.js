import axios from '../api/axios';

const useApi = () => {
    const getChannels = async () => {
        const response = await axios.get('/getChannelData');
        return response.data;
    };

    const getMessages = async (channel_name) => {
        const response = await axios.get('/getMessageData', { params: { channel_name } });
        return response.data;
    };

    return { getChannels, getMessages };
};

export default useApi;