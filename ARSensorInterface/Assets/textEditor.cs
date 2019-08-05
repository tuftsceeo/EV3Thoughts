// Lily Zhang and Mohammed Emun
// 8/5/19
// Handles IoT communication and visualization setup
// This version uses MQTT communication and does not contain sound/AR extension

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Security.Cryptography.X509Certificates;
using uPLibrary.Networking.M2Mqtt.Messages;
using uPLibrary.Networking.M2Mqtt;
using System.Net.Security;
using TMPro;
using MiniJSON; // https://gist.github.com/darktable/1411710


public class textEditor : MonoBehaviour
{
    // login variables
    public static string url;
    public static string user;
    public static string pass;

    // visualizations
    public GameObject forward_line;
    public GameObject right_line;
    public GameObject left_line;
    public GameObject needle_for_angle;   
    public GameObject cone_for_distance;
    public GameObject sphere_for_color;
    public GameObject sphere_for_touch;
    public GameObject angle_visual;
    public GameObject all_data_panel;
    public GameObject all_arrows; 

    // initialization for visualizations
    Vector3 temp;
    Vector3 temp_2;
    Vector3 temp_3;
    Vector3 temp_4;
    Vector3 temp_5;
    private TMPro.TextMeshPro tmProh;
    public TextMeshProUGUI tmpText;
    private object distReading = 0;
    private object colorReading = 0;
    private object angleReading = 0;
    private object touchReading = 0;
    private object forwardReading = 0;
    private object rightReading = 0;
    private object leftReading = 0;
    private object batteryReading = 0; 
    public static object scriptReading = "hello there";
    public SimpleHealthBar BatteryPower;

    // Sensor menu dropdown variables
    public TMPro.TMP_Dropdown select_visualization;
    public TMPro.TMP_InputField x_input;
    public TMPro.TMP_InputField y_input;
    public TMPro.TMP_InputField z_input;
    static Vector3 color_save;
    static Vector3 ultrasonic_save;
    static Vector3 touch_save;
    static Vector3 gyro_save;
    static Vector3 data_save;
    static Vector3 movement_save;
    private double x_mov_total_val;
    private double y_mov_total_val;
    private double z_mov_total_val;
    private bool apply;

    // MQTT variables
    private MqttClient client;
    private string broker = "iot.eclipse.org";

    // Start is called before the first frame update
    void Start()
    {
        // initialize visualization locations
        if (PlayerPrefs.GetInt("player_prefs_color") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("color_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("color_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("color_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            sphere_for_color.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("color_transform_x"), PlayerPrefs.GetFloat("color_transform_y"), PlayerPrefs.GetFloat("color_transform_z"));
        }
        if (PlayerPrefs.GetInt("player_prefs_cone") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("cone_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("cone_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("cone_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            cone_for_distance.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("cone_transform_x"), PlayerPrefs.GetFloat("cone_transform_y"), PlayerPrefs.GetFloat("cone_transform_z"));
        }
        if (PlayerPrefs.GetInt("player_prefs_touch") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("touch_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("touch_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("touch_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            sphere_for_touch.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("touch_transform_x"), PlayerPrefs.GetFloat("touch_transform_y"), PlayerPrefs.GetFloat("touch_transform_z"));
        }
        if (PlayerPrefs.GetInt("player_prefs_gyro") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("gyro_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("gyro_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("gyro_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            angle_visual.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("gyro_transform_x"), PlayerPrefs.GetFloat("gyro_transform_y"), PlayerPrefs.GetFloat("gyro_transform_z"));
        }
        if (PlayerPrefs.GetInt("player_prefs_data") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("color_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("color_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("color_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            all_data_panel.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("data_transform_x"), PlayerPrefs.GetFloat("data_transform_y"), PlayerPrefs.GetFloat("data_transform_z"));
        }
        if (PlayerPrefs.GetInt("player_prefs_arrows") == 1)
        {
            x_input.text = (PlayerPrefs.GetFloat("arrows_transform_x")).ToString();
            x_mov_total_val = double.Parse(x_input.text);
            y_input.text = (PlayerPrefs.GetFloat("arrows_transform_y")).ToString();
            y_mov_total_val = double.Parse(y_input.text);
            z_input.text = (PlayerPrefs.GetFloat("arrows_transform_z")).ToString();
            z_mov_total_val = double.Parse(z_input.text);
            all_arrows.transform.localPosition = new Vector3(PlayerPrefs.GetFloat("arrows_transform_x"), PlayerPrefs.GetFloat("arrows_transform_y"), PlayerPrefs.GetFloat("arrows_transform_z"));
        }

        // initialize panel text
        tmProh = GetComponent<TextMeshPro>() ?? gameObject.AddComponent<TextMeshPro>();
        tmpText.text = "LOADING...";
        tmProh.text = tmpText.text;

        // initialize MQTT connection
        client = new MqttClient(broker);
        // register to message received 
        client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;
        string clientId = System.Guid.NewGuid().ToString();
        try
        {
            client.Connect(clientId);
            Debug.Log("CONNECTED");
        }
        catch (System.Exception e)
        {
            Debug.LogError("CONNECTION ERROR: " + e);
            
            // also print in text panel?
        }
        // subscribe to the topic "topic/EV3ARProject" with QoS 1
        client.Subscribe(new string[] { "topic/EV3ARProject" }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
        
        //StartCoroutine(GetRequest());
    }


    // Update is called once per frame
    void Update()
    {
        Debug.Log("INSIDE UPDATE");
        // Battery Power
        //float battery_power = .78F;
        Debug.Log("BATTERY READING INSIDE UPDATE IS " + batteryReading);
        // check if any values are null; if so, break
        // if batteryReading is null, so are the rest
        if (batteryReading == null) {
            return;
        }

        float battery_power = float.Parse(batteryReading.ToString());

        if (battery_power < 1 && battery_power > .50)
        {
            BatteryPower.UpdateColor(Color.green);
        }
        else if (battery_power < .50 && battery_power > .25)
        {
            BatteryPower.UpdateColor(Color.yellow);
        }
        else if (battery_power < .25 && battery_power > 0)
        {
            BatteryPower.UpdateColor(Color.red);
        }
        BatteryPower.UpdateBar(battery_power, 1);

        string touch_output;
        if (touchReading.ToString() == "1")
            touch_output = "True";
        else if (touchReading.ToString() == "0")
            touch_output = "False";
        else
            touch_output = "what the heck";


        // update text panel display
        Debug.Log("PRINTING STRING INSIDE UPDATE");
        string output = "Distance: " + distReading.ToString() + "cm" + "\n" + "Angle: " + angleReading.ToString() + "\n" + "Color: " + colorReading.ToString() + "\n" + "Touch: " + touch_output;
        Debug.Log(output);
        tmProh.text = output;
        tmpText.text = output;

        string color = colorReading.ToString();
        Color32 brown = new Color32(114, 96, 96, 255);
        // sets text bubble to corresponding color reading
        switch (color)
        {

            case "white":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.white;
                break;
            case "red":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.red;
                break;
            case "yellow":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.yellow;
                break;
            case "green":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.green;
                break;
            case "blue":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.blue;
                break;
            case "brown":
                sphere_for_color.GetComponent<Renderer>().material.color = brown;
                break;
            case "black":
                sphere_for_color.GetComponent<Renderer>().material.color = Color.black;
                break;
            default:
                sphere_for_color.GetComponent<Renderer>().material.color = Color.grey;
                break;
        }
        // This is where the cone updates
        double size_cone = double.Parse(distReading.ToString());
        // Convert to inches
        size_cone = size_cone/3.2;
        // Convert to cm
        size_cone = size_cone / 2.54;
        float size_cone_new = (float)size_cone;
        temp = cone_for_distance.transform.localScale;
        temp.z = size_cone_new;
        temp.y = size_cone_new/3;
        temp.x = size_cone_new/3;
        cone_for_distance.transform.localScale = temp;

        // This is where the sphere for touch updates
        float sphere_touch = float.Parse(touchReading.ToString());
        temp_2 = sphere_for_touch.transform.localScale;
        //Debug.Log("the touch is-----" + sphere_touch);
        temp_2.z = sphere_touch/4;
        temp_2.y = sphere_touch/4;
        temp_2.x = sphere_touch/4;
        sphere_for_touch.transform.localScale = temp_2;

        // This is where the angle is measured
        float angle = float.Parse(angleReading.ToString());
        needle_for_angle.transform.rotation = Quaternion.Euler(0, 0, angle);

        // This is where the forward is shown
        float line_forward = float.Parse(forwardReading.ToString());
        temp_3 = forward_line.transform.localScale;
        temp_3.z = line_forward;
        temp_3.y = line_forward;
        temp_3.x = line_forward;
        forward_line.transform.localScale = temp_3;

        // This is where the right is shown
        float line_right = float.Parse(rightReading.ToString());
        temp_4 = right_line.transform.localScale;
        temp_4.z = line_right;
        temp_4.y = line_right;
        temp_4.x = line_right;
        right_line.transform.localScale = temp_4;

        // This is where the left is shown
        float line_left = float.Parse(leftReading.ToString());
        temp_5 = left_line.transform.localScale;
        temp_5.z = line_left;
        temp_5.y = line_left;
        temp_5.x = line_left;
        left_line.transform.localScale = temp_5;

        // CODE FOR DROPDOWN
        switch (select_visualization.value)
        {
            case 0:
                x_input.text = (sphere_for_color.transform.localPosition.x).ToString();
                y_input.text = (sphere_for_color.transform.localPosition.y).ToString();
                z_input.text = (sphere_for_color.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);

                if (x_plus.x_plus_apply == true)
                {
                    apply = true; 
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true; 
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true; 
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_color", 1);
                    sphere_for_color.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("color_transform_x", sphere_for_color.transform.localPosition.x);
                    PlayerPrefs.SetFloat("color_transform_y", sphere_for_color.transform.localPosition.y);
                    PlayerPrefs.SetFloat("color_transform_z", sphere_for_color.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
            case 1:
                x_input.text = (cone_for_distance.transform.localPosition.x).ToString();
                y_input.text = (cone_for_distance.transform.localPosition.y).ToString();
                z_input.text = (cone_for_distance.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);

                if (x_plus.x_plus_apply == true)
                {
                    apply = true;
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true;
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true;
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_cone", 1);
                    cone_for_distance.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("cone_transform_x", cone_for_distance.transform.localPosition.x);
                    PlayerPrefs.SetFloat("cone_transform_y", cone_for_distance.transform.localPosition.y);
                    PlayerPrefs.SetFloat("cone_transform_z", cone_for_distance.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
            case 2:
                x_input.text = (sphere_for_touch.transform.localPosition.x).ToString();
                y_input.text = (sphere_for_touch.transform.localPosition.y).ToString();
                z_input.text = (sphere_for_touch.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);

                if (x_plus.x_plus_apply == true)
                {
                    apply = true;
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true;
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true;
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_touch", 1);
                    sphere_for_touch.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("touch_transform_x", sphere_for_touch.transform.localPosition.x);
                    PlayerPrefs.SetFloat("touch_transform_y", sphere_for_touch.transform.localPosition.y);
                    PlayerPrefs.SetFloat("touch_transform_z", sphere_for_touch.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
            case 3:
                x_input.text = (angle_visual.transform.localPosition.x).ToString();
                y_input.text = (angle_visual.transform.localPosition.y).ToString();
                z_input.text = (angle_visual.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);

                if (x_plus.x_plus_apply == true)
                {
                    apply = true;
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true;
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true;
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_gyro", 1);
                    angle_visual.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("gyro_transform_x", angle_visual.transform.localPosition.x);
                    PlayerPrefs.SetFloat("gyro_transform_y", angle_visual.transform.localPosition.y);
                    PlayerPrefs.SetFloat("gyro_transform_z", angle_visual.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
            case 4:
                x_input.text = (all_data_panel.transform.localPosition.x).ToString();
                y_input.text = (all_data_panel.transform.localPosition.y).ToString();
                z_input.text = (all_data_panel.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);


                if (x_plus.x_plus_apply == true)
                {
                    apply = true;
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true;
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true;
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_data", 1);
                    all_data_panel.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("data_transform_x", all_data_panel.transform.localPosition.x);
                    PlayerPrefs.SetFloat("data_transform_y", all_data_panel.transform.localPosition.y);
                    PlayerPrefs.SetFloat("data_transform_z", all_data_panel.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
            case 5:
                x_input.text = (all_arrows.transform.localPosition.x).ToString();
                y_input.text = (all_arrows.transform.localPosition.y).ToString();
                z_input.text = (all_arrows.transform.localPosition.z).ToString();
                x_mov_total_val = double.Parse(x_input.text);
                y_mov_total_val = double.Parse(y_input.text);
                z_mov_total_val = double.Parse(z_input.text);

                if (x_plus.x_plus_apply == true)
                {
                    apply = true;
                    x_mov_total_val += .5;
                    x_input.text = x_mov_total_val.ToString();
                    x_plus.apply_equals_false();
                }
                if (X_minus.x_minus_apply == true)
                {
                    apply = true;
                    x_mov_total_val -= .5;
                    x_input.text = x_mov_total_val.ToString();
                    X_minus.apply_equals_false();
                }
                if (Y_plus.y_plus_apply == true)
                {
                    apply = true;
                    y_mov_total_val += .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_plus.apply_equals_false();
                }
                if (Y_minus.y_minus_apply == true)
                {
                    apply = true;
                    y_mov_total_val -= .5;
                    y_input.text = y_mov_total_val.ToString();
                    Y_minus.apply_equals_false();
                }
                if (Z_plus.z_plus_apply == true)
                {
                    apply = true;
                    z_mov_total_val += .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_plus.apply_equals_false();
                }
                if (Z_minus.z_minus_apply == true)
                {
                    apply = true;
                    z_mov_total_val -= .5;
                    z_input.text = z_mov_total_val.ToString();
                    Z_minus.apply_equals_false();
                }
                if (apply == true)
                {
                    PlayerPrefs.SetInt("player_prefs_arrows", 1);
                    all_arrows.transform.localPosition = new Vector3(float.Parse(x_input.text), float.Parse(y_input.text), float.Parse(z_input.text));
                    PlayerPrefs.SetFloat("arrows_transform_x", all_arrows.transform.localPosition.x);
                    PlayerPrefs.SetFloat("arrows_transform_y", all_arrows.transform.localPosition.y);
                    PlayerPrefs.SetFloat("arrows_transform_z", all_arrows.transform.localPosition.z);
                    apply = false;
                    break;
                }
                else
                    break;
        }
    }


    // get sensor reading from Thingworx 
    IEnumerator GetRequest()
    {
        for (;;)
        {
            Debug.Log("INFORMATION: ");
            Debug.Log(url);
            Debug.Log(user);
            Debug.Log(pass);
            UnityWebRequest request = new UnityWebRequest(url);
            request.SetRequestHeader("AUTHORIZATION", authenticate(user, pass));
            request.SetRequestHeader("Accept", "application/json");
            request.SetRequestHeader("Content-Type", "application/json");
            request.downloadHandler = new DownloadHandlerBuffer();
            yield return request.SendWebRequest();

            //Debug.Log("passed send web request");

            if (request.isNetworkError)
            {
                Debug.Log("Network Error");
            }
            if (request.isHttpError)        
            {
                Debug.Log("HTTP error :(");
            }
            else if (!request.downloadHandler.isDone)
            {
                Debug.Log("didn't download properly");
            }
            else
            {
                // Show results as text
                // Debug.Log("now trying to display downloaded info");
                Debug.Log(request.downloadHandler.text);

                // deserialize json?
                // https://gist.github.com/darktable/1411710
                var dict = Json.Deserialize(request.downloadHandler.text) as Dictionary<string, object>;

                // https://stackoverflow.com/questions/22739791/parse-nested-json-with-minijson-unity3d/22745634#22745634
                // data is passed as dictionary within a list
                List<object> rows = dict["rows"] as List<object>;
                Dictionary<string, object> rowData = rows[0] as Dictionary<string, object>;
                Debug.Log("printing out sensor readings");

                distReading = rowData["distance"];
                Debug.Log(distReading);
                colorReading = rowData["color"];
                Debug.Log(colorReading);
                angleReading = rowData["angle"];
                Debug.Log(angleReading);
                touchReading = rowData["touch"];
                Debug.Log(touchReading);
                forwardReading = rowData["forward"];
                Debug.Log(forwardReading);
                rightReading = rowData["right"];
                Debug.Log(rightReading);
                leftReading = rowData["left"];
                Debug.Log(leftReading);
                scriptReading = rowData["script"];
                batteryReading = (string)rowData["power"];
                Debug.Log(batteryReading); 
            }

        }

    }

    // create authentication setRequestHeader for password-protected site
    // from https://stackoverflow.com/questions/39482954/unitywebrequest-embedding-user-password-data-for-http-basic-authentication-not
    string authenticate(string username, string password)
    {
        string auth = username + ":" + password;
        auth = System.Convert.ToBase64String(System.Text.Encoding.GetEncoding("ISO-8859-1").GetBytes(auth));
        auth = "Basic " + auth;
        return auth;
    }


    // Handles incoming MQTT messages
    // Sets visualization variables with updated values
    void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {
        Debug.Log("INSIDE MQTT MSG PUBLISH RECEIVEED");
        // handle message received 
        string msg = System.Text.Encoding.UTF8.GetString(e.Message);
        Debug.Log("Received message from " + e.Topic + " : " + msg);

        // deserialize json?
        // https://gist.github.com/darktable/1411710
        var rowData = Json.Deserialize(msg) as Dictionary<string, object>;

        //// put all property names into a list
        //List<string> keyVals = new List<string>(rowData.Keys);
        //foreach (string key1 in keyVals)
        //{
        //    Debug.Log(key1 + ": " + rowData[key1]);
        //}

        Debug.Log("PRINTING ACTUAL VALUES");
        distReading = rowData["distance"];
        Debug.Log("distance is " + distReading);
        colorReading = rowData["color"];
        Debug.Log("color is " + colorReading);
        angleReading = rowData["angle"];
        Debug.Log("angle is " + angleReading);
        touchReading = rowData["touch"];
        Debug.Log("touch is " + touchReading);
        forwardReading = rowData["forward"];
        Debug.Log("forward is " + forwardReading);
        rightReading = rowData["right"];
        Debug.Log("right is " + rightReading);
        leftReading = rowData["left"];
        Debug.Log("left is " + leftReading);
        //scriptReading = rowData["script"];
        //Debug.Log("script is " + scriptReading);
        batteryReading = rowData["power"];
        Debug.Log("power is " + batteryReading);

    }
}

