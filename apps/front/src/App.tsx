import { HomeLayout } from "./components/templates/HomeLayout"

import { Link } from "@tanstack/react-router"

export default function App() {

  return(
      <HomeLayout>
        <nav>
          <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
          </ul>
        </nav>
      </HomeLayout>
  );
}
