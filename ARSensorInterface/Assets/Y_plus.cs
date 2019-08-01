using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Y_plus : MonoBehaviour
{
    public static bool y_plus_apply;

    public void change_apply()
    {
        y_plus_apply = !y_plus_apply;
    }
    public static void apply_equals_false()
    {
        y_plus_apply = false;
    }

}
