import "./icon.css";

import compassIcon from "/src/assets/icons/compass.svg";
import homeIcon from "/src/assets/icons/home.svg";
import listPlusIcon from "/src/assets/icons/list-plus.svg";
import magnifyingGlassIcon from "/src/assets/icons/magnifying-glass.svg";
import pencilIcon from "/src/assets/icons/pencil.svg";
import plusIcon from "/src/assets/icons/plus.svg";
import signOutIcon from "/src/assets/icons/sign-out.svg";
import trendUpIcon from "/src/assets/icons/trend-up.svg";
import xIcon from "/src/assets/icons/x.svg";

const icons = {
    compass: compassIcon,
    home: homeIcon,
    listPlus: listPlusIcon,
    magnifyingGlass: magnifyingGlassIcon,
    pencil: pencilIcon,
    plus: plusIcon,
    signOut: signOutIcon,
    trendUp: trendUpIcon,
    x: xIcon,
}

function Icon({name, size = "md", alt = ""}) {
    return (
        <img
            src={icons[name]}
            alt={alt}
            className={`icon icon-${size}`}
        />
    );
}

export default Icon;
