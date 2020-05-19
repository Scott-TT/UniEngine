<?php

/**
 * @param array $params
 * @param array $params['coordinates']
 * @param string $params['ownerID']
 * @param string | null $params['moonName']
 * @param number | null $params['moonCreationChance']
 * @param number | null $params['fixedDiameter']
 */
function CreateOneMoonRecord($params) {
    global $_Lang;

    $coordinates = $params['coordinates'];

    $QryGetMoonGalaxyData = "SELECT `galaxy_id`, `id_moon` FROM {{table}} WHERE `galaxy` = '{$coordinates['galaxy']}' AND `system` = '{$coordinates['system']}' AND `planet` = '{$coordinates['planet']}';";
    $MoonGalaxy = doquery($QryGetMoonGalaxyData, 'galaxy', true);
    if($MoonGalaxy['id_moon'] == 0)
    {
        $QryGetMoonPlanetData = "SELECT `id`, `temp_min`, `temp_max` FROM {{table}} WHERE `galaxy` = '{$coordinates['galaxy']}' AND `system` = '{$coordinates['system']}' AND `planet` = '{$coordinates['planet']}';";
        $MoonPlanet = doquery($QryGetMoonPlanetData, 'planets', true);

        if($MoonPlanet['id'] != 0)
        {
            if(!isset($params['fixedDiameter']) || !($params['fixedDiameter'] >= 2000 && $params['fixedDiameter'] <= 10000))
            {
                $Diameter_Min = 2000 + ($params['moonCreationChance'] * 100);
                $Diameter_Max = 6000 + ($params['moonCreationChance'] * 200);
                $Diameter = rand($Diameter_Min, $Diameter_Max);
            }
            else
            {
                $Diameter = $params['fixedDiameter'];
            }
            $RandTemp = rand(10, 45);
            $mintemp = $MoonPlanet['temp_min'] - $RandTemp;
            $maxtemp = $MoonPlanet['temp_max'] - $RandTemp;

            $newMoonName = (
                !empty($params['moonName']) ?
                    $params['moonName'] :
                    $_Lang['sys_moon']
            );

            $QryInsertMoonInPlanet = "INSERT INTO {{table}} SET ";
            $QryInsertMoonInPlanet .= "`name` = '{$newMoonName}', ";
            $QryInsertMoonInPlanet .= "`id_owner` = '{$params['ownerID']}', ";
            $QryInsertMoonInPlanet .= "`galaxy` = '{$coordinates['galaxy']}', ";
            $QryInsertMoonInPlanet .= "`system` = '{$coordinates['system']}', ";
            $QryInsertMoonInPlanet .= "`planet` = '{$coordinates['planet']}', ";
            $QryInsertMoonInPlanet .= "`last_update` = UNIX_TIMESTAMP(), ";
            $QryInsertMoonInPlanet .= "`planet_type` = 3, ";
            $QryInsertMoonInPlanet .= "`image` = 'mond', ";
            $QryInsertMoonInPlanet .= "`diameter` = '{$Diameter}', ";
            $QryInsertMoonInPlanet .= "`field_max` = 1, ";
            $QryInsertMoonInPlanet .= "`temp_min` = '{$maxtemp}', ";
            $QryInsertMoonInPlanet .= "`temp_max` = '{$mintemp}', ";
            $QryInsertMoonInPlanet .= "`metal` = 0, ";
            $QryInsertMoonInPlanet .= "`metal_perhour` = 0, ";
            $QryInsertMoonInPlanet .= "`metal_max` = '".BASE_STORAGE_SIZE."', ";
            $QryInsertMoonInPlanet .= "`crystal` = 0, ";
            $QryInsertMoonInPlanet .= "`crystal_perhour` = 0, ";
            $QryInsertMoonInPlanet .= "`crystal_max` = '".BASE_STORAGE_SIZE."', ";
            $QryInsertMoonInPlanet .= "`deuterium` = 0, ";
            $QryInsertMoonInPlanet .= "`deuterium_perhour` = 0, ";
            $QryInsertMoonInPlanet .= "`deuterium_max` = '".BASE_STORAGE_SIZE."';";
            doquery($QryInsertMoonInPlanet, 'planets');

            // Select CreatedMoon ID
            $QrySelectPlanet = "SELECT `id` FROM {{table}} WHERE `galaxy` = '{$coordinates['galaxy']}' AND `system` = '{$coordinates['system']}' AND `planet` = '{$coordinates['planet']}' AND `planet_type` = 3;";
            $GetPlanetID = doquery($QrySelectPlanet, 'planets', true);

            $QryUpdateMoonInGalaxy = "UPDATE {{table}} SET ";
            $QryUpdateMoonInGalaxy .= "`id_moon` = '{$GetPlanetID['id']}' ";
            $QryUpdateMoonInGalaxy .= "WHERE `galaxy_id` = {$MoonGalaxy['galaxy_id']};";
            doquery($QryUpdateMoonInGalaxy, 'galaxy');

            return $GetPlanetID['id'];
        }
    }

    return false;
}

?>
