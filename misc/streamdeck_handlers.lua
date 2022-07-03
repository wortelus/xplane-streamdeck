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

create_command( "FlyWithLua/streamdeck_handler/flt_alt_down_start", "flt alt down start handler", "command_begin(\"laminar/B738/knob/flt_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_down_end", "flt alt down end handler", "command_end(\"laminar/B738/knob/flt_alt_press_dn\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_up_start", "flt alt up start handler", "command_begin(\"laminar/B738/knob/flt_alt_press_up\")", "", "" )
create_command( "FlyWithLua/streamdeck_handler/flt_alt_up_end", "flt alt up end handler", "command_end(\"laminar/B738/knob/flt_alt_press_up\")", "", "" )

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