import React from 'react';

const ListView = ({ results, type }) => {
    if (!results || results.length === 0) {
        return <p>No results found.</p>;
    }

    return (
        <div>
            <h2 className="text-2xl font-bold mb-2">Results</h2>
            <ul className="list-disc pl-5">
                {results.map((item) => (
                    <li key={item.id} className="mb-2 p-2 border rounded">
                        <h3 className="font-bold">{item.name}</h3>
                        {type === 'cafes' && <p>{item.address}</p>}
                        {type === 'cafes' && item.open_date && <p>Opened: {item.open_date}</p>}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ListView;