export default function Card({ title, content }) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm mx-auto">
        <h2 className="text-2xl font-semibold mb-4">{title}</h2>
        <p className="text-gray-600">{content}</p>
      </div>
    );
  }