export default function Button({ content, onClick }) {
    return (
        <button className="btn m-4 bg-neutral-900/30 border-none border-neutral-600 hover:bg-neutral-800/30" onClick={onClick}>
            {content}
        </button>
    );
}