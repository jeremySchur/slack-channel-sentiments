
const SearchAndFilter = ({ searchQuery, setSearchQuery, sortOrder, setSortOrder }) => {
    return (
        <div className="p-4 border-b border-gray-200 flex gap-2">
            <input
                type="text"
                placeholder="Search channels..."
                className="min-w-1/2 p-2 border border-gray-300 rounded-lg"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />

            <select
                className="min-w-1/2 p-2 border border-gray-300 rounded-lg"
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
            >
                <option value="desc">Highest Sentiment</option>
                <option value="asc">Lowest Sentiment</option>
            </select>
        </div>
    );
};

export default SearchAndFilter;