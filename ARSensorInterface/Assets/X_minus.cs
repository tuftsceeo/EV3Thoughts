using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class X_minus : MonoBehaviour
{
    public static bool x_minus_apply;

    public void change_apply()
    {
        x_minus_apply = !x_minus_apply;
    }
    public static void apply_equals_false()
    {
        x_minus_apply = false;
    }

}
