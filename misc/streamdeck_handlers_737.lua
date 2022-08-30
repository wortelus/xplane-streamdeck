if not (PLANE_ICAO == "B736" or PLANE_ICAO == "B737" or PLANE_ICAO == "B738" or PLANE_ICAO == "B739" or PLANE_ICAO == "B38M") then
	return
end
	
create_command( "FlyWithLua/streamdeck_handler/fire_test_right_start", "fire test zibo right start handler", "command_begin(\"laminar/B738/toggle_switch/fire_test_rgt\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fire_test_right_end", "fire test zibo right end handler", "command_end(\"laminar/B738/toggle_switch/fire_test_rgt\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fire_test_left_start", "fire test zibo left start handler", "command_begin(\"laminar/B738/toggle_switch/fire_test_lft\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fire_test_left_end", "fire test zibo left end handler", "command_end(\"laminar/B738/toggle_switch/fire_test_lft\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/capt_fire_warn_start", "Capt fire warn light start handler", "command_begin(\"laminar/B738/push_button/fire_bell_light1\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_fire_warn_end", "Capt fire warn light end handler", "command_end(\"laminar/B738/push_button/fire_bell_light1\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/capt_master_caution_start", "Capt master caution light start handler", "command_begin(\"laminar/B738/push_button/master_caution1\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_master_caution_end", "Capt master caution light end handler", "command_end(\"laminar/B738/push_button/master_caution1\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/capt_six_pack_start", "Capt six pack start handler", "command_begin(\"laminar/B738/push_button/capt_six_pack\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_six_pack_end", "Capt six pack end handler", "command_end(\"laminar/B738/push_button/capt_six_pack\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fo_six_pack_start", "F/O six pack start handler", "command_begin(\"laminar/B738/push_button/capt_six_pack\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fo_six_pack_end", "F/O six pack end handler", "command_end(\"laminar/B738/push_button/capt_six_pack\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/at_arm_start", "", "command_begin(\"laminar/B738/autopilot/autothrottle_arm_toggle\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/at_arm_end", "", "command_end(\"laminar/B738/autopilot/autothrottle_arm_toggle\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/fo_course_up_start", "", "command_begin(\"laminar/B738/autopilot/course_copilot_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fo_course_up_end", "", "command_end(\"laminar/B738/autopilot/course_copilot_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fo_course_dn_start", "", "command_begin(\"laminar/B738/autopilot/course_copilot_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fo_course_dn_end", "", "command_end(\"laminar/B738/autopilot/course_copilot_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_course_up_start", "", "command_begin(\"laminar/B738/autopilot/course_pilot_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_course_up_end", "", "command_end(\"laminar/B738/autopilot/course_pilot_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_course_dn_start", "", "command_begin(\"laminar/B738/autopilot/course_pilot_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/capt_course_dn_end", "", "command_end(\"laminar/B738/autopilot/course_pilot_dn\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/mins_dn_start", "", "command_begin(\"laminar/B738/pfd/dh_pilot_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/mins_dn_end", "", "command_end(\"laminar/B738/pfd/dh_pilot_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/mins_up_start", "", "command_begin(\"laminar/B738/pfd/dh_pilot_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/mins_up_end", "", "command_end(\"laminar/B738/pfd/dh_pilot_up\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/baro_dn_start", "", "command_begin(\"laminar/B738/pilot/barometer_down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/baro_dn_end", "", "command_end(\"laminar/B738/pilot/barometer_down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/baro_up_start", "", "command_begin(\"laminar/B738/pilot/barometer_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/baro_up_end", "", "command_end(\"laminar/B738/pilot/barometer_up\")", "", "" )

dataref("fixed_left_ldg_light", "laminar/B738/switch/land_lights_left_pos", "writable")
function landing_lights_toggle_left()
	if fixed_left_ldg_light == 0 then
		fixed_left_ldg_light = 1
	else
		fixed_left_ldg_light = 0
	end
end

dataref("fixed_right_ldg_light", "laminar/B738/switch/land_lights_right_pos", "writable")
function landing_lights_toggle_right()
	if fixed_right_ldg_light == 0 then
		fixed_right_ldg_light = 1
	else
		fixed_right_ldg_light = 0
	end
end

create_command("FlyWithLua/streamdeck_handler/fixed_left_ldg_lights", "", "landing_lights_toggle_left()", "", "")
create_command("FlyWithLua/streamdeck_handler/fixed_right_ldg_lights", "", "landing_lights_toggle_right()", "", "")

dataref("left_turnoff_light", "laminar/B738/toggle_switch/rwy_light_left", "writable")
function turnoff_lights_toggle_left()
	if left_turnoff_light == 0 then
		left_turnoff_light = 1
	else
		left_turnoff_light = 0
	end
end

dataref("right_turnoff_light", "laminar/B738/toggle_switch/rwy_light_right", "writable")
function turnoff_lights_toggle_right()
	if right_turnoff_light == 0 then
		right_turnoff_light = 1
	else
		right_turnoff_light = 0
	end
end

create_command("FlyWithLua/streamdeck_handler/left_turnoff_lights", "", "turnoff_lights_toggle_left()", "", "")
create_command("FlyWithLua/streamdeck_handler/right_turnoff_lights", "", "turnoff_lights_toggle_right()", "", "")

create_command( "FlyWithLua/streamdeck_handler/apu_switch_dn_start", "", "command_begin(\"laminar/B738/spring_toggle_switch/APU_start_pos_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/apu_switch_dn_end", "", "command_end(\"laminar/B738/spring_toggle_switch/APU_start_pos_dn\")", "", "" )


create_command( "FlyWithLua/streamdeck_handler/grd_call_start", "", "command_begin(\"laminar/B738/push_button/grd_call\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/grd_call_end", "", "command_end(\"laminar/B738/push_button/grd_call\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/attend_start", "", "command_begin(\"laminar/B738/push_button/attend\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/attend_end", "", "command_end(\"laminar/B738/push_button/attend\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/ident_start", "", "command_begin(\"laminar/B738/push_button/transponder_ident_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ident_end", "", "command_end(\"laminar/B738/push_button/transponder_ident_dn\")", "", "" )

dataref("n1_set_adjust", "laminar/B738/toggle_switch/n1_set_adjust", "writable")
function n1_set_adjust_dn()
	if n1_set_adjust > 0.7 then
		n1_set_adjust = n1_set_adjust - 0.001
	end
end

function n1_set_adjust_up()
	if n1_set_adjust < 1.03 then
		n1_set_adjust = n1_set_adjust + 0.001
	end
end

function n1_set_adjust_dn_1()
	if n1_set_adjust > 0.7 then
		n1_set_adjust = n1_set_adjust - 0.01
	end
end

function n1_set_adjust_up_1()
	if n1_set_adjust < 1.03 then
		n1_set_adjust = n1_set_adjust + 0.01
	end
end

create_command("FlyWithLua/streamdeck_handler/n1_dn", "", "n1_set_adjust_dn()", "", "")
create_command("FlyWithLua/streamdeck_handler/n1_up", "", "n1_set_adjust_up()", "", "")
create_command("FlyWithLua/streamdeck_handler/n1_dn_1", "", "n1_set_adjust_dn_1()", "", "")
create_command("FlyWithLua/streamdeck_handler/n1_up_1", "", "n1_set_adjust_up_1()", "", "")

create_command("FlyWithLua/streamdeck_handler/ff_up_start", "", "command_begin(\"laminar/B738/toggle_switch/fuel_flow_up\")", "", "")
create_command("FlyWithLua/streamdeck_handler/ff_up_end", "", "command_end(\"laminar/B738/toggle_switch/fuel_flow_up\")", "", "")
create_command("FlyWithLua/streamdeck_handler/ff_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/fuel_flow_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/ff_dn_end", "", "command_end(\"laminar/B738/toggle_switch/fuel_flow_dn\")", "", "")

create_command("FlyWithLua/streamdeck_handler/ap_prst_start", "", "command_begin(\"laminar/B738/push_button/ap_light_pilot\")", "", "")
create_command("FlyWithLua/streamdeck_handler/ap_prst_end", "", "command_end(\"laminar/B738/push_button/ap_light_pilot\")", "", "")
create_command("FlyWithLua/streamdeck_handler/at_prst_start", "", "command_begin(\"laminar/B738/push_button/at_light_pilot\")", "", "")
create_command("FlyWithLua/streamdeck_handler/at_prst_end", "", "command_end(\"laminar/B738/push_button/at_light_pilot\")", "", "")
create_command("FlyWithLua/streamdeck_handler/fmc_prst_start", "", "command_begin(\"laminar/B738/push_button/fms_light_pilot\")", "", "")
create_command("FlyWithLua/streamdeck_handler/fmc_prst_end", "", "command_end(\"laminar/B738/push_button/fms_light_pilot\")", "", "")

create_command("FlyWithLua/streamdeck_handler/allign_analog_start", "", "command_begin(\"laminar/B738/button/allign_analog_horiz\")", "", "")
create_command("FlyWithLua/streamdeck_handler/allign_analog_end", "", "command_end(\"laminar/B738/button/allign_analog_horiz\")", "", "")

dataref("fp_1", "laminar/B738/fuel/fuel_tank_pos_lft1", "writable")
dataref("fp_2", "laminar/B738/fuel/fuel_tank_pos_lft2", "writable")
dataref("fp_3", "laminar/B738/fuel/fuel_tank_pos_rgt1", "writable")
dataref("fp_4", "laminar/B738/fuel/fuel_tank_pos_rgt2", "writable")
dataref("fp_5", "laminar/B738/fuel/fuel_tank_pos_ctr1", "writable")
dataref("fp_6", "laminar/B738/fuel/fuel_tank_pos_ctr2", "writable")

function fp_1_toggle()
	if fp_1 == 1.0 then
		fp_1 = 0.0
		return
	end
	fp_1 = 1.0
end

function fp_2_toggle()
	if fp_2 == 1.0 then
		fp_2 = 0.0
		return
	end
	fp_2 = 1.0
end

function fp_3_toggle()
	if fp_3 == 1.0 then
		fp_3 = 0.0
		return
	end
	fp_3 = 1.0
end

function fp_4_toggle()
	if fp_4 == 1.0 then
		fp_4 = 0.0
		return
	end
	fp_4 = 1.0
end

function fp_5_toggle()
	if fp_5 == 1.0 then
		fp_5 = 0.0
		return
	end
	fp_5 = 1.0
end

function fp_6_toggle()
	if fp_6 == 1.0 then
		fp_6 = 0.0
		return
	end
	fp_6 = 1.0
end

create_command("FlyWithLua/streamdeck_handler/fp1_toggle", "", "fp_1_toggle()", "", "")
create_command("FlyWithLua/streamdeck_handler/fp2_toggle", "", "fp_2_toggle()", "", "")
create_command("FlyWithLua/streamdeck_handler/fp3_toggle", "", "fp_3_toggle()", "", "")
create_command("FlyWithLua/streamdeck_handler/fp4_toggle", "", "fp_4_toggle()", "", "")
create_command("FlyWithLua/streamdeck_handler/fp5_toggle", "", "fp_5_toggle()", "", "")
create_command("FlyWithLua/streamdeck_handler/fp6_toggle", "", "fp_6_toggle()", "", "")


create_command("FlyWithLua/streamdeck_handler/gen1_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/gen1_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/gen1_dn_end", "", "command_end(\"laminar/B738/toggle_switch/gen1_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/apu_gen1_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/apu_gen1_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/apu_gen1_dn_end", "", "command_end(\"laminar/B738/toggle_switch/apu_gen1_dn\")", "", "")

create_command("FlyWithLua/streamdeck_handler/gen2_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/gen2_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/gen2_dn_end", "", "command_end(\"laminar/B738/toggle_switch/gen2_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/apu_gen2_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/apu_gen2_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/apu_gen2_dn_end", "", "command_end(\"laminar/B738/toggle_switch/apu_gen2_dn\")", "", "")

create_command("FlyWithLua/streamdeck_handler/gpu_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/gpu_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/gpu_dn_end", "", "command_end(\"laminar/B738/toggle_switch/gpu_dn\")", "", "")

create_command("FlyWithLua/streamdeck_handler/yaw_damper_start", "", "command_begin(\"laminar/B738/toggle_switch/yaw_dumper\")", "", "")
create_command("FlyWithLua/streamdeck_handler/yaw_damper_end", "", "command_end(\"laminar/B738/toggle_switch/yaw_dumper\")", "", "")

create_command("FlyWithLua/streamdeck_handler/alt_flaps_up_start", "", "command_begin(\"laminar/B738/toggle_switch/alt_flaps_ctrl_up\")", "", "")
create_command("FlyWithLua/streamdeck_handler/alt_flaps_up_end", "", "command_end(\"laminar/B738/toggle_switch/alt_flaps_ctrl_up\")", "", "")
create_command("FlyWithLua/streamdeck_handler/alt_flaps_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/alt_flaps_ctrl_dn\")", "", "")
create_command("FlyWithLua/streamdeck_handler/alt_flaps_dn_end", "", "command_end(\"laminar/B738/toggle_switch/alt_flaps_ctrl_dn\")", "", "")

create_command( "FlyWithLua/streamdeck_handler/flt_alt_down_start", "flt alt down start handler", "command_begin(\"laminar/B738/knob/flt_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_down_end", "flt alt down end handler", "command_end(\"laminar/B738/knob/flt_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_up_start", "flt alt up start handler", "command_begin(\"laminar/B738/knob/flt_alt_press_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_up_end", "flt alt up end handler", "command_end(\"laminar/B738/knob/flt_alt_press_up\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/air_valve_left_start", "", "command_begin(\"laminar/B738/toggle_switch/air_valve_manual_left\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/air_valve_left_end", "flt alt up end handler", "command_end(\"laminar/B738/toggle_switch/air_valve_manual_left\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/air_valve_right_start", "", "command_begin(\"laminar/B738/toggle_switch/air_valve_manual_right\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/air_valve_right_end", "flt alt up end handler", "command_end(\"laminar/B738/toggle_switch/air_valve_manual_right\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/land_alt_down_start", "land alt down start handler", "command_begin(\"laminar/B738/knob/land_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/land_alt_down_end", "land alt down end handler", "command_end(\"laminar/B738/knob/land_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/land_alt_up_start", "land alt up start handler", "command_begin(\"laminar/B738/knob/land_alt_press_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/land_alt_up_end", "land alt up end handler", "command_end(\"laminar/B738/knob/land_alt_press_up\")", "", "" )

create_command("FlyWithLua/streamdeck_handler/gpws_test_start", "", "command_begin(\"laminar/B738/push_button/gpws_test\")", "", "")
create_command("FlyWithLua/streamdeck_handler/gpws_fire_test_end", "", "command_end(\"laminar/B738/push_button/gpws_test\")", "", "")

create_command("FlyWithLua/streamdeck_handler/cargo_fire_test_start", "", "command_begin(\"laminar/B738/push_button/cargo_fire_test_push\")", "", "")
create_command("FlyWithLua/streamdeck_handler/cargo_fire_test_end", "", "command_end(\"laminar/B738/push_button/cargo_fire_test_push\")", "", "")

create_command("FlyWithLua/streamdeck_handler/mach1_test_start", "", "command_begin(\"laminar/B738/push_button/mach_warn1_test\")", "", "")
create_command("FlyWithLua/streamdeck_handler/mach1_test_end", "", "command_end(\"laminar/B738/push_button/mach_warn1_test\")", "", "")
create_command("FlyWithLua/streamdeck_handler/mach2_test_start", "", "command_begin(\"laminar/B738/push_button/mach_warn2_test\")", "", "")
create_command("FlyWithLua/streamdeck_handler/mach2_test_end", "", "command_end(\"laminar/B738/push_button/mach_warn2_test\")", "", "")

create_command("FlyWithLua/streamdeck_handler/stall1_test_start", "", "command_begin(\"laminar/B738/push_button/stall_test1_press\")", "", "")
create_command("FlyWithLua/streamdeck_handler/stall1_test_end", "", "command_end(\"laminar/B738/push_button/stall_test1_press\")", "", "")
create_command("FlyWithLua/streamdeck_handler/stall2_test_start", "", "command_begin(\"laminar/B738/push_button/stall_test2_press\")", "", "")
create_command("FlyWithLua/streamdeck_handler/stall2_test_end", "", "command_end(\"laminar/B738/push_button/stall_test2_press\")", "", "")

create_command( "FlyWithLua/streamdeck_handler/ap_speed_up_start", "", "command_begin(\"sim/autopilot/airspeed_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_speed_up_end", "", "command_end(\"sim/autopilot/airspeed_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_speed_dn_start", "", "command_begin(\"sim/autopilot/airspeed_down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_speed_dn_end", "", "command_end(\"sim/autopilot/airspeed_down\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/ap_heading_up_start", "", "command_begin(\"laminar/B738/autopilot/heading_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_heading_up_end", "", "command_end(\"laminar/B738/autopilot/heading_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_heading_dn_start", "", "command_begin(\"laminar/B738/autopilot/heading_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_heading_dn_end", "", "command_end(\"laminar/B738/autopilot/heading_dn\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/ap_altitude_up_start", "", "command_begin(\"laminar/B738/autopilot/altitude_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_altitude_up_end", "", "command_end(\"laminar/B738/autopilot/altitude_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_altitude_dn_start", "", "command_begin(\"laminar/B738/autopilot/altitude_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_altitude_dn_end", "", "command_end(\"laminar/B738/autopilot/altitude_dn\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/ap_vs_up_start", "", "command_begin(\"sim/autopilot/vertical_speed_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_vs_up_end", "", "command_end(\"sim/autopilot/vertical_speed_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_vs_dn_start", "", "command_begin(\"sim/autopilot/vertical_speed_down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/ap_vs_dn_end", "", "command_end(\"sim/autopilot/vertical_speed_down\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/trip_reset_start", "", "command_begin(\"laminar/B738/push_button/bleed_trip_reset\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/trip_reset_end", "", "command_end(\"laminar/B738/push_button/bleed_trip_reset\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/alt_horn_start", "", "command_begin(\"laminar/B738/alert/alt_horn_cutout\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/alt_horn_end", "", "command_end(\"laminar/B738/alert/alt_horn_cutout\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/win_ovht_test_up_start", "", "command_begin(\"laminar/B738/toggle_switch/window_ovht_test_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/win_ovht_test_up_end", "", "command_end(\"laminar/B738/toggle_switch/window_ovht_test_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/win_ovht_test_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/window_ovht_test_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/win_ovht_test_dn_end", "", "command_end(\"laminar/B738/toggle_switch/window_ovht_test_dn\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/alt_flaps_dn_start", "", "command_begin(\"laminar/B738/toggle_switch/alt_flaps_ctrl_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/alt_flaps_test_dn_end", "", "command_end(\"laminar/B738/toggle_switch/alt_flaps_ctrl_dn\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/forward_start", "", "command_begin(\"sim/general/forward\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/forward_end", "", "command_end(\"sim/general/forward\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fforward_start", "", "command_begin(\"sim/general/forward_fast\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fforward_end", "", "command_end(\"sim/general/forward_fast\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/backward_start", "", "command_begin(\"sim/general/backward\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/backward_end", "", "command_end(\"sim/general/backward\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fbackward_start", "", "command_begin(\"sim/general/backward_fast\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/fbackward_end", "", "command_end(\"sim/general/backward_fast\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/up_start", "", "command_begin(\"sim/general/up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/up_end", "", "command_end(\"sim/general/up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/right_start", "", "command_begin(\"sim/general/right\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/right_end", "", "command_end(\"sim/general/right\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/down_start", "", "command_begin(\"sim/general/down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/down_end", "", "command_end(\"sim/general/down\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/left_start", "", "command_begin(\"sim/general/left\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/left_end", "", "command_end(\"sim/general/left\")", "", "" )

create_command( "FlyWithLua/streamdeck_handler/exting_left_start", "", "command_begin(\"laminar/B738/toggle_switch/exting_test_lft\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/exting_left_end", "", "command_end(\"laminar/B738/toggle_switch/exting_test_lft\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/exting_right_start", "", "command_begin(\"laminar/B738/toggle_switch/exting_test_rgt\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/exting_right_end", "", "command_end(\"laminar/B738/toggle_switch/exting_test_rgt\")", "", "" )