import React from 'react';

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip">
                <p className="label">{`${label}`}</p>
                <p className="intro">{`Revenue: $${payload[0].value.toLocaleString()}`}</p>
                <p className="desc">
                    <strong>Prediction:</strong> We predict a 10% increase in sales for this product next month.
                </p>
            </div>
        );
    }

    return null;
};

export default CustomTooltip;
