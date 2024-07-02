import os
import git


INCLUDE_TYPES = set([
    'py', 'h', 'hpp', 'c', 'cpp', 'cu', 'js', 'java', 'm', 'ipynb', 'glsl', 'sv',
    'bash', 'sh', 'launch', 'do',
    'html', 'css', 'md', 'tex', 'bib',
    'gitignore', 'gitmodules', 'gitattributes',
])

def get_commit_info(repo_path):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        raise ValueError("Not a valid Git repository.")

    repo = git.Repo(repo_path)
    commits_info = []

    for commit in repo.iter_commits(repo.head.ref.name):
        info = {
            'date': commit.authored_datetime,
            'message': commit.message.strip(),
            'byte_delta': { '': 0 },
            'line_delta': { '': 0 },
            'file_delta': { '': 0 },
        }
        print(commit.message.strip())

        def add_blob(blob, sign):
            # ftype = blob.mime_type
            ftype = blob.name.split('.')[-1]
            if ftype not in INCLUDE_TYPES:
                return
            # byte
            if ftype not in info['byte_delta']:
                info['byte_delta'][ftype] = 0
            delta = sign * blob.size
            info['byte_delta'][ftype] += delta
            info['byte_delta'][''] += delta
            # line
            try:
                data = blob.data_stream.read().decode('utf-8')
                delta = sign * (data.count('\n')+1)
                if ftype not in info['line_delta']:
                    info['line_delta'][ftype] = 0
                info['line_delta'][ftype] += delta
                info['line_delta'][''] += delta
            except UnicodeDecodeError:
                pass
            # file
            if ftype not in info['file_delta']:
                info['file_delta'][ftype] = 0
            info['file_delta'][ftype] += sign
            info['file_delta'][''] += sign

        if len(commit.parents) == 0:
            diffs = commit.diff(git.NULL_TREE)
        else:
            diffs = commit.parents[0].diff(commit)
        for diff in diffs:
            if diff.a_blob:
                add_blob(diff.a_blob, -1)
            if diff.b_blob:
                add_blob(diff.b_blob, 1)

        commits_info.append(info)

    return commits_info


def plot_all(commits, field="commit"):
    import numpy as np
    # import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.dates import date2num

    x = date2num([c['date'] for c in commits])
    if field == "commit":
        y = [1] * len(commits)
    else:
        y = [c[field+'_delta'][''] for c in commits]

    plt.figure()

    bw = 0.02*(max(x)-min(x))
    n = 1000
    xs = np.linspace(min(x)-2*bw, max(x)+2*bw, n)
    ys = np.zeros(xs.shape)
    for xi, yi in zip(x, y):
        # s = bw / np.sqrt(2*np.pi)
        s = bw
        ys += yi * np.exp(-(xs-xi)**2/(2*s**2)) / (np.sqrt(2*np.pi)*s)
    plt.plot(xs, ys)
    plt.fill(np.concatenate((xs, [xs[-1], xs[0]])),
             np.concatenate((ys, [0.0, 0.0])), alpha=0.5)

    plt.gca().xaxis_date()
    plt.xlabel('Date')
    plt.ylabel('Average daily (σ={:.3g} days)'.format(bw))
    plt.title(f"Repository `{repo_path.split('/')[-1]}`, by {field}s")
    plt.show()


def plot_per_type(commits, field):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.dates import date2num

    all_types = {}
    for c in commits:
        for ftype, delta in c[field+'_delta'].items():
            if ftype not in all_types:
                all_types[ftype] = 0
            all_types[ftype] += delta
    all_types = sorted(all_types.items(), key=lambda _: -_[1])
    print(all_types)

    plt.figure()

    x = date2num([c['date'] for c in commits])
    y = [c['line_delta'][''] for c in commits]

    bw = 0.02*(max(x)-min(x))
    n = 1000
    xs = np.linspace(min(x)-0*bw, max(x)+0*bw, n)

    for ftype, fcount in all_types:
        x, y = [], []
        for c in commits:
            if ftype in c[field+'_delta']:
                x.append(date2num(c['date']))
                y.append(c[field+'_delta'][ftype])

        ys = np.zeros(xs.shape)
        for xi, yi in zip(x, y):
            ys += yi * np.exp(-(xs-xi)**2/(2*bw**2)) / (np.sqrt(2*np.pi)*bw)
        if ftype == '':
            plt.plot(xs, ys, 'k--', alpha=0.5)
        else:
            plt.plot(xs, ys, label=ftype)
            plt.fill(np.concatenate((xs, [xs[-1], xs[0]])),
                    np.concatenate((ys, [0.0, 0.0])), alpha=0.5)

    plt.legend()
    plt.gca().xaxis_date()
    plt.xlabel('Date')
    plt.ylabel('Average daily (σ={:.3g} days)'.format(bw))
    plt.title(f"Repository `{repo_path.split('/')[-1]}`, by {field}s of code")
    plt.show()


if __name__ == "__main__":
    # repo_path = '../../spirulae'
    # repo_path = '../../harry7557558.github.io'
    repo_path = '../../Graphics'
    commits = get_commit_info(repo_path)

    # for commit in commits:
    #     print(f"Commit Date: {commit['date']}")
    #     print(f"Commit Message: {commit['message']}")
    #     print("Byte delta:", commit['byte_delta'])
    #     print("Line delta:", commit['line_delta'])
    #     print("File delta:", commit['file_delta'])
    #     print(end="\n")

    # plot_all(commits)
    plot_per_type(commits, 'line')
    # plot_per_type(commits, 'byte')
