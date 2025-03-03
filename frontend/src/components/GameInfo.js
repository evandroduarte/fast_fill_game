import { jsxs as _jsxs, jsx as _jsx } from "react/jsx-runtime";
export const GameInfo = ({ redCount, blueCount, timeElapsed, playerColor, gameStatus, winner }) => {
    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    };
    const getStatusMessage = () => {
        if (gameStatus === 'waiting') {
            return 'Waiting for another player to join...';
        }
        else if (gameStatus === 'finished') {
            if (winner === 'tie') {
                return 'Game over! It\'s a tie!';
            }
            else {
                return `Game over! ${winner === playerColor ? 'You won!' : 'You lost!'}`;
            }
        }
        else {
            return 'Game in progress...';
        }
    };
    return (_jsxs("div", { className: "game-info", children: [_jsxs("div", { className: "time-elapsed", children: ["Time: ", formatTime(timeElapsed)] }), _jsxs("div", { className: "square-counter", children: [_jsxs("span", { className: `red-count ${playerColor === 'red' ? 'my-color' : ''}`, children: ["Red: ", redCount] }), _jsxs("span", { className: `blue-count ${playerColor === 'blue' ? 'my-color' : ''}`, children: ["Blue: ", blueCount] })] }), _jsx("div", { className: "status-message", children: getStatusMessage() }), playerColor && (_jsxs("div", { className: "player-info", children: ["You are playing as ", _jsx("span", { className: playerColor, children: playerColor })] }))] }));
};
