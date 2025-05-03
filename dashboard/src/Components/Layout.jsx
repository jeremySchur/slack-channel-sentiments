
const Layout = ({ children }) => {
    return (
        <div className="w-full mt-4 flex flex-col xl:flex-row gap-4">
            {children}
        </div>
    );
};

export default Layout;