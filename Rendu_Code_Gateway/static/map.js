var poseTopic = new ROSLIB.Topic({
                ros         : ros,
                name        : '/robot_pose',
                messageType : 'geometry_msgs/Pose'
            });


            poseTopic.subscribe(function(message) {
                        console.log('In pose subscribe callback');

                    // Formats the pose for outputting.
                        var now = new Date();
                        var position = 'x: ' + message.position.x
                            + ', y: ' + message.position.y
                            + ', z: 0.0';
                        var orientation = 'x: ' + message.orientation.x
                            + ', y: ' + message.orientation.y
                            + ', z: ' + message.orientation.z
                            + ', w: ' + message.orientation.w;
                        });

                    // Create the main viewer.
                        var viewer = new ROS2D.Viewer({
                            divID : 'mapRobot',
                            width : 400,
                            height : 400
                        });

                    // Setup the map client.
                        var gridClient = new ROS2D.OccupancyGridClient({
                            ros : ros,
                            rootObject : viewer.scene
                        });

                    // Scale the canvas to fit to the map
                        gridClient.on('change', function() {
                            viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
                            viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
                            displayPoseMarker();
                        });

                    // ----------------------------------------------------------------------
                    // Showing the pose on the map
                    // ----------------------------------------------------------------------

                        function displayPoseMarker() {
                    // Create a marker representing the robot.
                            var robotMarker = new ROS2D.NavigationArrow({
                              size : 12,
                              strokeSize : 1,
                              fillColor : createjs.Graphics.getRGB(255, 128, 0, 0.66),
                              pulse : true
                            });
                            robotMarker.visible = false;
                            console.log('creating robotMarkr: ');

                    // Add the marker to the 2D scene.
                            gridClient.rootObject.addChild(robotMarker);
                            var initScaleSet = false;

                            console.log('creating topic listener: ');
                    // Subscribe to the robot's pose updates.
                            var poseListener = new ROSLIB.Topic({
                              ros : ros,
                              name : '/odom',
                              messageType : 'nav_msgs/Odometry',
                              throttle_rate : 100
                            });

                            poseListener.subscribe(function(pose) {

                    // Orientate the marker based on the robot's pose.

                              //console.log('Got Pose data:', pose.pose.pose.position.x, pose.pose.pose.position.y );
                              robotMarker.x = pose.pose.pose.position.x;
                              robotMarker.y = -pose.pose.pose.position.y ;
                              //console.log('Pose updated: ', robotMarker.x);
                              if (!initScaleSet) {
                                robotMarker.scaleX = 1.0 / viewer.scene.scaleX;
                                robotMarker.scaleY = 1.0 / viewer.scene.scaleY;
                                initScaleSet = true;
                              }
                              robotMarker.rotation = viewer.scene.rosQuaternionToGlobalTheta(pose.pose.pose.orientation);
                              robotMarker.visible = true;
                            });
                        }
