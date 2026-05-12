import Button from "../components/Button/Button.jsx";
import Footer from "../components/Footer/Footer.jsx";
import Navbar from "../components/Navigation/Navbar.jsx";
import Icon from "../components/Icon/Icon.jsx";

function HomePage() {
    return (
        <div className="page-wrap">
            <Navbar/>
            <div className="main-wrap">
                <section className="section-padding-lg">
                    {/* Hero section */}
                    <div className="container-lg">
                        <div className="header-wrap">
                            <h1 className="text-color-brand">MotorMinder</h1>
                            <p>MotorMinder is a car maintenance tracking and recommendation application designed to help
                                vehicle owners better understand, manage, and maintain their vehicles' health. A lot of
                                drivers have a hard time keeping track of routine maintenance, like oil changes, tire
                                rotations, inspections, etc. This can lead to unnecessary repairs, wasted money, and
                                reduced vehicle lifespan. This application aims to consolidate vehicle information to
                                give the user valuable maintenance recommendations based on vehicle condition data.</p>
                        </div>
                    </div>
                </section>
                <section className="section-padding-lg">
                    <div className="container-lg">
                        {/* Features section */}
                        <div className="features-wrap">
                            <div className="features-content-wrap">
                                <div className="features-content">
                                    <Icon name="plus" size="md" alt="Plus Icon"/>
                                    <div className="utility-wrap-vertical">
                                        <text className="features-label">Add your car</text>
                                        <p className="features-subtext">Input your vehicle details and let the app learn
                                            your maintenance history</p>
                                    </div>
                                </div>
                                <div className="features-content">
                                    <Icon name="trendUp" size="md" alt="Trend Up Icon"/>
                                    <div className="utility-wrap-vertical">
                                        <text className="features-label">Track the work</text>
                                        <p className="features-subtext">Log services as they happen and watch your
                                            maintenance record grow</p>
                                    </div>
                                </div>
                                <div className="features-content">
                                    <Icon name="compass" size="md" alt="Compass Icon"/>
                                    <div className="utility-wrap-vertical">
                                        <text className="features-label">Get guidance</text>
                                        <p className="features-subtext">Receive smart recommendations based on your
                                            car’s actual condition and needs</p>
                                    </div>
                                </div>
                            </div>
                            <img alt="Blank image" src="/assets/car-mechanic-1.png"
                                 style={{height: "400px", width: "400px"}}/>
                        </div>
                    </div>
                </section>
                <section className="section-padding-lg">
                    {/* Sign up/login section */}
                    <div className="container-lg">
                        <div className="section-content-wrap">
                            <div className="header-wrap">
                                <h1>Take Control of Your Vehicle Maintenance</h1>
                                <p>Sign up to organize service records, track repairs, and never miss another
                                    maintenance milestone. Already registered? Log in to access your dashboard.</p>
                            </div>
                            <div className="button-group">
                                <Button text="Sign Up" link="/signup"/>
                                <Button text="Login" link="/login" variant="surface"/>
                            </div>
                            <img alt="Blank image" src="/assets/car-mechanic-2.png" style={{width: "100%"}}/>
                        </div>
                    </div>
                </section>
            </div>
            <Footer/>
        </div>
    )
}

export default HomePage;
