using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StabilizeObject : MonoBehaviour
{
    public GameObject speech_bubble;
    public GameObject angle;
    public GameObject angle_needle;
    public GameObject touch;

    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("starting stabilizer code");

    }

    // Update is called once per frame
    void Update()
    {
        speech_bubble.transform.LookAt(Camera.main.transform.position, Vector3.up);
        angle.transform.LookAt(Camera.main.transform.position, Vector3.up);
        angle_needle.transform.LookAt(Camera.main.transform.position, Vector3.up);
        touch.transform.LookAt(Camera.main.transform.position, Vector3.up);
    }

}
