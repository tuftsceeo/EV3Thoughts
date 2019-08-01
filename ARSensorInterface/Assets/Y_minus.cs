using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Y_minus : MonoBehaviour
{
    public static bool y_minus_apply;

    public void change_apply()
    {
        y_minus_apply = !y_minus_apply;
    }
    public static void apply_equals_false()
    {
        y_minus_apply = false;
    }

}
