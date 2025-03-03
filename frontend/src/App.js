import { jsx as _jsx } from "react/jsx-runtime";
import { GamePage } from './components/GamePage';
import './App.css';
function App() {
    return (_jsx("div", { className: "App", children: _jsx(GamePage, {}) }));
}
export default App;
