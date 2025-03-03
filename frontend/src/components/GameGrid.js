import { jsx as _jsx } from "react/jsx-runtime";
export const GameGrid = ({ grid, onCellClick, playerColor, isGameActive }) => {
    return (_jsx("div", { className: "game-grid", children: grid.map((row, rowIndex) => (_jsx("div", { className: "grid-row", children: row.map((cell, colIndex) => (_jsx("div", { className: `grid-cell ${cell !== 'empty' ? cell : ''}`, onClick: () => {
                    if (isGameActive && cell === 'empty' && playerColor) {
                        onCellClick(rowIndex, colIndex);
                    }
                } }, `${rowIndex}-${colIndex}`))) }, rowIndex))) }));
};
