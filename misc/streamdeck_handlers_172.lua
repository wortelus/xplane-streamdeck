if not (PLANE_ICAO == "C172") then
	return
end


-- Note these create command start and end make it so a key push can be held
-- added 172  This file is just for the stock 172  There are come commands for a G5 equipped 172 but they do not effect the stock 172
-- Aug. 2022
-- Aileron Trims
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_left_start", "172 Aileron Trim Left handler", "command_begin(\"sim/flight_controls/aileron_trim_left\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_left_end", "172 Aileron Trim Left handler", "command_end(\"sim/flight_controls/aileron_trim_left\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_center_start", "172 Aileron Trim Center handler", "command_begin(\"sim/flight_controls/aileron_trim_center\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_center_end", "172 Aileron Trim Center handler", "command_end(\"sim/flight_controls/aileron_trim_center\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_right_start", "172 Aileron Trim Right handler", "command_begin(\"sim/flight_controls/aileron_trim_right\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_ail_right_end", "172 Aileron Trim Right handler", "command_end(\"sim/flight_controls/aileron_trim_right\")", "", "" )
 
 -- Rudder Trims
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_left_start", "172 Rudder Trim Left handler", "command_begin(\"sim/flight_controls/rudder_trim_left\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_left_end", "172 Rudder Trim Left handler", "command_end(\"sim/flight_controls/rudder_trim_left\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_center_start", "172 Rudder Trim Center handler", "command_begin(\"sim/flight_controls/rudder_trim_center\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_center_end", "172 Rudder Trim Center handler", "command_end(\"sim/flight_controls/rudder_trim_center\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_right_start", "172 Rudder Trim Right handler", "command_begin(\"sim/flight_controls/rudder_trim_right\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_rud_right_end", "172 Rudder Trim Right handler", "command_end(\"sim/flight_controls/rudder_trim_right\")", "", "" )
 
-- Pitch Trims 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_down_start", "172 Pitch Trim Down handler", "command_begin(\"sim/flight_controls/pitch_trim_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_down_end", "172 Pitch Trim Down handler", "command_end(\"sim/flight_controls/pitch_trim_down\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_takeoff_start", "172 Pitch Trim Takeoff handler", "command_begin(\"sim/flight_controls/pitch_trim_takeoff\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_takeoff_end", "172 Pitch Trim Takeoff handler", "command_end(\"sim/flight_controls/pitch_trim_takeoff\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_up_start", "172 Pitch Trim Up handler", "command_begin(\"sim/flight_controls/pitch_trim_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_trim_pitch_up_end", "172 Pitch Trim Up handler", "command_end(\"sim/flight_controls/pitch_trim_up\")", "", "" )

-- G5 Keys

-- G5 AI 
 create_command( "FlyWithLua/streamdeck_handler/172_ai_KnobL_start", "172 AI KnobL handler", "command_begin(\"afm/g5/cmd/a/knobL\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_ai_KnobL_end", "172 AI KnobL handler", "command_end(\"afm/g5/cmd/a/knobL\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_ai_knobPush_start", "172 AI KnobPush handler", "command_begin(\"afm/g5/cmd/a/knobPush\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_ai_KnobPush_end", "172 AI KnobPush handler", "command_end(\"afm/g5/cmd/a/knobPush\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_ai_KnobR_start", "172 AI KnobR handler", "command_begin(\"afm/g5/cmd/a/knobR\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_ai_KnobR_end", "172 AI KnobR handler", "command_end(\"afm/g5/cmd/a/knobR\")", "", "" )

-- G5 HSI

 create_command( "FlyWithLua/streamdeck_handler/172_hsi_KnobL_start", "172 HSI KnobL handler", "command_begin(\"afm/g5/cmd/b/knobL\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_hsi_KnobL_end", "172 HSI KnobL handler", "command_end(\"afm/g5/cmd/b/knobL\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_hsi_knobPush_start", "172 HSI KnobPush handler", "command_begin(\"afm/g5/cmd/b/knobPush\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_hsi_KnobPush_end", "172 HSI KnobPush handler", "command_end(\"afm/g5/cmd/b/knobPush\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_hsi_KnobR_start", "172 HSI KnobR handler", "command_begin(\"afm/g5/cmd/b/knobR\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_hsi_KnobR_end", "172 HSI KnobR handler", "command_end(\"afm/g5/cmd/b/knobR\")", "", "" )

-- G5 Keys End

-- Upper panel ALT, NAV1 CDI NAV2 CDI Start

-- ALT

-- Not using too large a change
--  create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_down_start", "172 ALT Barometer Down handler", "command_begin(\"sim/instruments/barometer_down\")", "", "" )
--  create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_down_end", "172 ALT Barometer Down handler", "command_end(\"sim/instruments/barometer_down\")", "", "" )


 create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_push_start", "172 ALT Barometer Push handler", "command_begin(\"sim/instruments/barometer_2992\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_push_end", "172 ALT Barometer Push handler", "command_end(\"sim/instruments/barometer_2992\")", "", "" )

-- Not using too large a change
--  create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_up_start", "172 ALT Barometer Up handler", "command_begin(\"sim/instruments/barometer_up\")", "", "" )
--  create_command( "FlyWithLua/streamdeck_handler/172_alt_barometer_up_end", "172 ALT Barometer Up handler", "command_end(\"sim/instruments/barometer_up\")", "", "" )

-- CDI's
 create_command( "FlyWithLua/streamdeck_handler/172_nav1_cdi_down_start", "172 NAV1 CDI Down handler", "command_begin(\"sim/radios/obs1_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_nav1_cdi_down_end", "172 NAV1 CDI Down handler", "command_end(\"sim/radios/obs1_down\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_nav1_cdi_up_start", "172 NAV1 CDI Up handler", "command_begin(\"sim/radios/obs1_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_nav1_cdi_up_end", "172 NAV1 CDI Up handler", "command_end(\"sim/radios/obs1_up\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_nav2_cdi_down_start", "172 NAV2 CDI Down handler", "command_begin(\"sim/radios/obs2_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_nav2_cdi_down_end", "172 NAV2 CDI Down handler", "command_end(\"sim/radios/obs2_down\")", "", "" )
 
 create_command( "FlyWithLua/streamdeck_handler/172_nav2_cdi_up_start", "172 NAV2 CDI Up handler", "command_begin(\"sim/radios/obs2_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_nav2_cdi_up_end", "172 NAV2 CDI Up handler", "command_end(\"sim/radios/obs2_up\")", "", "" )

-- Upper panel ALT, NAV1 CDI NAV2 CDI End

-- 172 Non G5 Keys AI HSI Start
-- AI
 create_command( "FlyWithLua/streamdeck_handler/172_ai_down_start", "172 AI Down handler", "command_begin(\"sim/instruments/ah_ref_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_ai_down_end", "172 AI Down handler", "command_end(\"sim/instruments/ah_ref_down\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_ai_up_start", "172 AI Up handler", "command_begin(\"sim/instruments/ah_ref_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_ai_up_end", "172 AI Up handler", "command_end(\"sim/instruments/ah_ref_up\")", "", "" )

--- DG
-- DG Left Knob Note a push on this key will sync the heading to the compass but it doesn't need to be a push and hold
 create_command( "FlyWithLua/streamdeck_handler/172_dg_sync_down_start", "172 DG Sync Down handler", "command_begin(\"sim/instruments/DG_sync_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_dg_sync_down_end", "172 DG Sync Down handler", "command_end(\"sim/instruments/DG_sync_down\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_dg_sync_up_start", "172 DG Sync Up handler", "command_begin(\"sim/instruments/DG_sync_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_dg_sync_up_end", "172 DG Sync Up handler", "command_end(\"sim/instruments/DG_sync_up\")", "", "" )
 
-- DG Right Knob
 create_command( "FlyWithLua/streamdeck_handler/172_dg_heading_down_start", "172 DG Heading Down handler", "command_begin(\"sim/autopilot/heading_down\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_dg_heading_down_end", "172 DG Heading Down handler", "command_end(\"sim/autopilot/heading_down\")", "", "" )

 create_command( "FlyWithLua/streamdeck_handler/172_dg_heading_up_start", "172 DG Heading Up handler", "command_begin(\"sim/autopilot/heading_up\")", "", "" )
 create_command( "FlyWithLua/streamdeck_handler/172_dg_heading_up_end", "172 DG Heading Up handler", "command_end(\"sim/autopilot/heading_up\")", "", "" )

-- 172 Non G5 Keys AI HSI  End


-- script to read the squawk code dataref and return 4 datarefs one for each digit
-- sim/cockpit/radios/transponder_code # 1234
-- 1200 -> 1, 2, 0, 0

---------------------------------------------------------------------------  Reading datarefs
dataref("squawkcode", "sim/cockpit/radios/transponder_code", "readonly") 
dataref("framer", "sim/operation/misc/frame_rate_period", "readonly") 

-------------------------------------------------------------------------------------  Create datarefs 
squawk1000 = create_dataref_table("FlyWithLua/streamdeck_handler/squawk1000", "Int")
squawk100 = create_dataref_table("FlyWithLua/streamdeck_handler/squawk100", "Int")
squawk10 = create_dataref_table("FlyWithLua/streamdeck_handler/squawk10", "Int")
squawk1 = create_dataref_table("FlyWithLua/streamdeck_handler/squawk1", "Int")
frame_rate = create_dataref_table("FlyWithLua/streamdeck_handler/frame_rate", "Float")  -- Frame Rate to pass to the Stream Deck
 
local SC1
local Squawk_hold

squawk1000[0] = 0
squawk100[0] = 0
squawk10[0] = 0
squawk1[0] = 0
frame_rate[0] = 0
Squawk_hold = 9999

function updatesquawk ()
   if Squawk_hold ~= squawkcode then
	  squawk1000[0] = squawkcode / 1000
      SC1= squawkcode % 1000
      squawk100[0] = SC1 / 100
      SC1 = SC1 % 100
      squawk10[0] = SC1 / 10
      squawk1[0]  = SC1 % 10
      Squawk_hold = squawkcode
	end
end

do_every_draw("updatesquawk()")

 function updateframe ()
	frame_rate[0] = 1/framer
 end
 do_often("updateframe()")  -- Every 1 Sec

	
-- End Added 172












