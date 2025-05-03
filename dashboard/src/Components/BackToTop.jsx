
const BackToTop = () => {
    const handleClick = () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };

    return (
        <button
            id="back_to_top"
            className="bg-primary text-white px-4 py-2 rounded-lg shadow-md"
            onClick={handleClick}
        >
            Back to Top
        </button>
    );
};

export default BackToTop;