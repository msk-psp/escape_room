import React, { useState, useEffect } from 'react';

const ContentSection = ({ title }) => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await fetch('http://localhost:8000/themes/');
                if (response.ok) {
                    const data = await response.json();
                    setItems(data.slice(0, 3)); // Displaying top 3 for now
                } else {
                    console.error(`Failed to fetch ${title}`);
                }
            } catch (error) {
                console.error(`Error fetching ${title}:`, error);
            }
        };

        fetchItems();
    }, [title]);

    return (
        <div className="mb-8">
            <h2 className="text-2xl font-bold mb-4">{title}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.length > 0 ? items.map(item => (
                    <div key={item.id} className="border p-4 rounded">
                        <h3 className="font-bold">{item.name}</h3>
                    </div>
                )) : (
                    <p>No items to display.</p>
                )}
            </div>
        </div>
    );
};

export default ContentSection;