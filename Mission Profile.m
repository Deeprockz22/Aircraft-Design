%% Flight Mission Profile Generator in MATLAB
% Generates a clean, textbook-style aircraft flight mission profile
% Includes: Take-off, Cruise (FL350), Descent, Loiter (FL250), Land, Diversion, and Reserve
% Initial flight length (Main mission): 12,500 km

clear; clc; close all;

%% 1. Create Figure
fig = figure('Name', 'Flight Mission Profile', ...
             'Color', 'w', ...
             'Position', [100, 100, 950, 680]);
ax = axes('Parent', fig);
hold(ax, 'on');

%% 2. Diagram Geometric Boundaries
x_min = 5;   x_max = 95;
y_min = 0;   y_max = 90;

% Outer rectangular frame (textbook style)
plot([x_min, x_max, x_max, x_min, x_min], ...
     [y_min, y_min, y_max, y_max, y_min], ...
     'k-', 'LineWidth', 1.6);

%% 3. Cruising Altitude Definition & Flight Levels
y_FL0   = 6.0;   % Ground level (FL0)
y_FL15  = 16.0;  % Initial departure level (FL15)
y_FL350 = 74.0;  % Cruising altitude level (FL350)

% Loiter altitude proportional to 25,000 ft:
y_FL250 = y_FL0 + (250 / 350) * (y_FL350 - y_FL0); % FL250 (54.6)

% FL0 (Ground level)
plot([x_min, x_max], [y_FL0, y_FL0], 'k:', 'LineWidth', 1.1);
text(40, y_FL0 + 2.2, 'FL0', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

% FL15
plot([x_min, x_max], [y_FL15, y_FL15], 'k:', 'LineWidth', 1.1);
text(40, y_FL15 + 2.2, 'FL15', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

% FL250 (Loiter level)
plot([x_min, x_max], [y_FL250, y_FL250], 'k:', 'LineWidth', 1.1);
text(61, y_FL250 + 2.2, 'FL250', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

% FL350 (Cruise level)
plot([x_min, x_max], [y_FL350, y_FL350], 'k:', 'LineWidth', 1.1);
text(36, y_FL350 + 2.4, 'FL350', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

%% 4. Vertical Phase Boundary Lines (Dashed)
x_to_cr  = 25;  % Take-off -> Cruise
x_cr_de  = 47;  % Cruise -> Descent
x_de_lo  = 57;  % Descent -> Loiter
x_lo_la  = 67;  % Loiter -> Land
x_la_di  = 76;  % Land -> Diversion

phase_divs = [x_to_cr, x_cr_de, x_de_lo, x_lo_la, x_la_di];
for x = phase_divs
    plot([x, x], [y_min, y_max], 'k--', 'LineWidth', 1.0);
end

%% 5. Top Phase Labels (Rotated 90 degrees)
font_opts = {'FontName', 'Times New Roman', 'FontSize', 12, ...
             'Rotation', 90, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left'};

text(9,  y_max - 5, 'Take-off',   font_opts{:});
text(28, y_max - 5, 'Cruise',     font_opts{:});
text(49, y_max - 5, 'Descent',    font_opts{:});
text(59, y_max - 5, 'Loiter',     font_opts{:});
text(69, y_max - 5, 'Land',       font_opts{:});
text(79, y_max - 5, 'Diversion',  font_opts{:});

%% 6. Flight Profile Trajectory (Cruising at FL350, Loiter at FL250)
x_profile = [
     5.0, ...  % Ground start
     8.0, ...  % Take-off roll begin
    11.5, ...  % Initial climb to FL15
    15.0, ...  % Level segment at FL15
    19.5, ...  % Intermediate climb
    25.0, ...  % Reach cruise altitude (FL350)
    47.0, ...  % End of cruise at FL350
    57.0, ...  % Reach loiter altitude (FL250)
    65.0, ...  % End of loiter at FL250
    72.0, ...  % Touchdown / landing at destination (FL0)
    76.0, ...  % Diversion decision
    82.5, ...  % Climb to alternate cruise altitude
    88.5, ...  % End of diversion cruise
    93.5, ...  % Alternate landing touchdown
    95.0       % Parking / shut-down
];

y_profile = [
    y_FL0, ...
    y_FL0, ...
    y_FL15, ...
    y_FL15, ...
    36.0, ...
    y_FL350, ...
    y_FL350, ...
    y_FL250, ...
    y_FL250, ...
    y_FL0, ...
    y_FL0, ...
    48.0, ...
    48.0, ...
    y_FL0, ...
    y_FL0
];

% Draw the flight trajectory curve
plot(x_profile, y_profile, 'k-', 'LineWidth', 2.4);

%% 7. Top Weight Labels & Downward Arrows (MTOW, Landing weight, ZFW)
draw_down_arrow(ax, 8.0,  y_max + 7.5, y_max, 'MTOW');
draw_down_arrow(ax, 72.0, y_max + 7.5, y_max, 'Landing weight');
draw_down_arrow(ax, 93.5, y_max + 7.5, y_max, 'ZFW');

%% 8. Bottom Dimension Brackets (Main mission, Reserve, Diversion)
% Vertical guide lines extending down from the frame
plot([x_min, x_min], [y_min, -26], 'k-',  'LineWidth', 0.8);
plot([8.0,   8.0],   [y_min, -18], 'k-',  'LineWidth', 0.8);
plot([57.0,  57.0],  [y_min, -18], 'k:',  'LineWidth', 0.8);
plot([72.0,  72.0],  [y_min, -18], 'k-',  'LineWidth', 0.8);
plot([76.0,  76.0],  [y_min, -10], 'k-',  'LineWidth', 0.8);
plot([93.5,  93.5],  [y_min, -26], 'k-',  'LineWidth', 0.8);

% 1. Main mission bracket with 12,500 km initial flight length
draw_dimension_bracket(ax, 8.0, 72.0, -7.0, 'Main mission (12,500 km)', false);

% 2. Diversion bracket (sub-segment)
draw_dimension_bracket(ax, 76.0, 93.5, -7.0, 'Diversion', false);

% 3. Reserve bracket (encompassing Loiter and Diversion)
draw_dimension_bracket(ax, 57.0, 93.5, -15.5, 'Reserve', true);

% 4. Total flight mission duration / fuel span
draw_dimension_bracket(ax, x_min, 93.5, -23.5, 'Flight time and fuel', false);

%% 9. Axis Settings
xlim([0, 100]);
ylim([-30, 105]);
axis(ax, 'off'); % Hide default axes for a clean publication-ready look

%% 10. Optional: Export High-Resolution Images (PNG/PDF)
% exportgraphics(fig, 'flight_mission_profile.png', 'Resolution', 300);
% exportgraphics(fig, 'flight_mission_profile.pdf', 'ContentType', 'vector');

disp('Flight mission profile diagram with FL250 and 12,500 km successfully generated in MATLAB!');


%% === HELPER FUNCTIONS ===

% Draw downward-pointing arrow with weight label
function draw_down_arrow(~, x, y_start, y_end, label_text)
    plot([x, x], [y_start, y_end], 'k-', 'LineWidth', 1.3);
    arr_w = 0.9;
    arr_h = 2.0;
    fill([x - arr_w, x + arr_w, x], ...
         [y_end + arr_h, y_end + arr_h, y_end], ...
         'k', 'EdgeColor', 'none');
    text(x, y_start + 1.2, label_text, ...
         'FontName', 'Times New Roman', 'FontSize', 12, ...
         'FontWeight', 'bold', 'FontAngle', 'italic', ...
         'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
end

% Draw horizontal double-ended dimension bracket with label
function draw_dimension_bracket(~, x1, x2, y, label_text, is_bold)
    plot([x1, x2], [y, y], 'k-', 'LineWidth', 1.2);
    arr_w = 1.6;
    arr_h = 1.0;
    fill([x1, x1 + arr_w, x1 + arr_w], [y, y + arr_h, y - arr_h], 'k', 'EdgeColor', 'none');
    fill([x2, x2 - arr_w, x2 - arr_w], [y, y + arr_h, y - arr_h], 'k', 'EdgeColor', 'none');
     
    weight = 'normal';
    if is_bold
        weight = 'bold';
    end
    text((x1 + x2)/2, y + 1.2, label_text, ...
         'FontName', 'Times New Roman', 'FontSize', 11, ...
         'FontWeight', weight, ...
         'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
end
