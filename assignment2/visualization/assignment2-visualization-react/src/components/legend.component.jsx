import { MapControl, withLeaflet } from "react-leaflet";
import L from "leaflet";

class Legend extends MapControl {
    createLeafletElement(props) {}

    componentDidMount() {
        const getColor = d => {
            return d > this.props.min+(this.props.max)*6
                ? "#800026"
                : d > this.props.min+(this.props.max)*5
                    ? "#BD0026"
                    : d > this.props.min+(this.props.max)*4
                        ? "#E31A1C"
                        : d > this.props.min+(this.props.max)*3
                            ? "#FC4E2A"
                            : d > this.props.min+(this.props.max)*2
                                ? "#FD8D3C"
                                : d > this.props.min+(this.props.max)
                                    ? "#FEB24C"
                                    : d > this.props.min
                                        ? "#FED976"
                                        : "#FFEDA0";
        };

        const legend = L.control({ position: "bottomright" });

        legend.onAdd = () => {
            const max = this.props.max, min = this.props.min;
            const div = L.DomUtil.create("div", "info legend");
            const grades = [
                min,
                min+(max),
                min+(max)*2,
                min+(max)*3,
                min+(max)*4,
                min+(max)*5,
                min+(max)*6,
                min+(max)*7
            ];
            let labels = [];
            let from;
            let to;

            for (let i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];

                labels.push(
                    '<i style="background:' +
                    getColor(from + 1) +
                    '"></i> ' +
                    from +
                    (to ? "&ndash;" + to : "+")
                );
            }

            div.innerHTML = labels.join("<br>");
            return div;
        };

        const { map } = this.props.leaflet;
        legend.addTo(map);
    }
}

export default withLeaflet(Legend);
