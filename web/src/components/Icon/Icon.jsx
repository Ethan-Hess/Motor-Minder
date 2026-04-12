import "./icon.css";

import compassIcon from "/assets/icons/compass.svg";
import listPlusIcon from "/assets/icons/list-plus.svg";
import magnifyingGlassIcon from "/assets/icons/magnifying-glass.svg";
import pencilIcon from "/assets/icons/pencil.svg";
import plusIcon from "/assets/icons/plus.svg";
import signOutIcon from "/assets/icons/sign-out.svg";
import trendUpIcon from "/assets/icons/trend-up.svg";

const icons = {
    compass: compassIcon,
    listPlus: listPlusIcon,
    magnifyingGlass: magnifyingGlassIcon,
    pencil: pencilIcon,
    plus: plusIcon,
    signOut: signOutIcon,
    trendUp: trendUpIcon,
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
