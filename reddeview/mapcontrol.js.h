class _mapControl
{
    Map map; //map object from google map api
    DirectionService direction; //direction service object

    element menu; //main menu bar element
    element menuShow; //custom button inserted into google map

    void menuSet(); //menu actions
    void mapButtons(); //custom buttons rendered by google map

    void roadLineDrawtest();
    void loadGeoJsonTest();

    void loadTracs();
}