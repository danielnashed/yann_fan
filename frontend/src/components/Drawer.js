export default function Drawer({ isOpen }) {
    return (
        <div className={`fixed top-0 left-0 h-full w-80 bg-neutral-900/60 transform transition-transform duration-300 ease-in-out ${
            isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
            <ul className="menu p-4">
                <li><a>Sidebar Item 1</a></li>
                <li><a>Sidebar Item 2</a></li>
            </ul>
        </div>
    );
}