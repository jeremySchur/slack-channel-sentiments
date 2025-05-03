
const Background = ({ children, className }) => {
  return (
    <div className={`w-full bg-[#F6F7F8] ${className || ""}`}>
      {children}
    </div>
  );
};

export default Background;